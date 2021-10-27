import { spin_button } from "./utils"
import { Presentation } from "./presenter/presentation";
import { BufferPresentation } from "./buffer_presenter/buffer_presentation";
import { FallbackPresentation } from "./fallback_presenter/fallback_presentation";

// used to load and update player settings
let CACHE_BATCH_SIZE = 5;
let PAST_SECTIONS_TO_BUFFER = 2;
let FUTURE_SECTIONS_TO_BUFFER = 5;
let USE_FALLBACK_LOADER = false;
let url_search_params = new URLSearchParams(location.search);

function load_url_params(): void {
    if (url_search_params.has("cache_batch_size"))
        CACHE_BATCH_SIZE = Number(url_search_params.get("cache_batch_size"));
    if (url_search_params.has("past_sections_to_buffer"))
        PAST_SECTIONS_TO_BUFFER = Number(url_search_params.get("past_sections_to_buffer"));
    if (url_search_params.has("future_sections_to_buffer"))
        FUTURE_SECTIONS_TO_BUFFER = Number(url_search_params.get("future_sections_to_buffer"));
    if (url_search_params.has("use_fallback_loader"))
        USE_FALLBACK_LOADER = url_search_params.get("use_fallback_loader") === "true";
}

// update url parameters and reload page
function update_url_params(): void {
    url_search_params.set("cache_batch_size", CACHE_BATCH_SIZE.toString());
    url_search_params.set("past_sections_to_buffer", FUTURE_SECTIONS_TO_BUFFER.toString());
    url_search_params.set("future_sections_to_buffer", PAST_SECTIONS_TO_BUFFER.toString());
    url_search_params.set("use_fallback_loader", USE_FALLBACK_LOADER.toString());

    window.history.replaceState({}, "", `${location.pathname}?${url_search_params.toString()}`);
    location.reload();
}

function create_presentation(): Presentation {
    if (USE_FALLBACK_LOADER) {
        console.log(`Using FallbackPresentation with a cache batch size of ${CACHE_BATCH_SIZE}`);
        return new FallbackPresentation(CACHE_BATCH_SIZE);
    }
    else {
        console.log(`Using BufferPresentation with ${FUTURE_SECTIONS_TO_BUFFER} sections to auto load, ${PAST_SECTIONS_TO_BUFFER} sections to keep and a cache batch size of ${CACHE_BATCH_SIZE}`);
        return new BufferPresentation(CACHE_BATCH_SIZE, FUTURE_SECTIONS_TO_BUFFER, PAST_SECTIONS_TO_BUFFER);
    }
}

function attach_ui(presentation: Presentation): void {
    let previous = document.getElementById("previous-section") as HTMLButtonElement;
    let restart = document.getElementById("restart-section") as HTMLButtonElement;
    let next = document.getElementById("next-section") as HTMLButtonElement;
    let fullscreen = document.getElementById("fullscreen") as HTMLButtonElement;
    let cache = document.getElementById("cache") as HTMLButtonElement;
    let update_settings = document.getElementById("update_settings") as HTMLButtonElement;

    // add callbacks
    previous.addEventListener("click", presentation.play_previous_section.bind(presentation));
    restart.addEventListener("click", presentation.restart_current_section.bind(presentation));
    next.addEventListener("click", presentation.play_next_section.bind(presentation));
    fullscreen.addEventListener("click", presentation.enter_fullscreen.bind(presentation));
    cache.addEventListener("click", () => {
        spin_button(cache);
        presentation.cache(() => {
            cache.remove();
        });
    });

    // set player setting values
    let cache_batch_size = document.getElementById("cache-batch-size") as HTMLInputElement;
    let past_sections_to_buffer = document.getElementById("past-sections-to-buffer") as HTMLInputElement;
    let future_sections_to_buffer = document.getElementById("future-sections-to-buffer") as HTMLInputElement;
    let use_buffer_loader = document.getElementById("fallback-loader-selected") as HTMLInputElement;
    let use_fallback_loader = document.getElementById("fallback-loader-selected") as HTMLInputElement;
    cache_batch_size.value = CACHE_BATCH_SIZE.toString();
    past_sections_to_buffer.value = PAST_SECTIONS_TO_BUFFER.toString();
    future_sections_to_buffer.value = FUTURE_SECTIONS_TO_BUFFER.toString();
    use_buffer_loader.checked = !USE_FALLBACK_LOADER;
    use_fallback_loader.checked = USE_FALLBACK_LOADER;

    // set callback
    update_settings.addEventListener("click", () => {
        CACHE_BATCH_SIZE = parseInt(cache_batch_size.value);
        PAST_SECTIONS_TO_BUFFER = parseInt(past_sections_to_buffer.value);
        FUTURE_SECTIONS_TO_BUFFER = parseInt(future_sections_to_buffer.value);
        // buffer-loader-selected doesn't have to be worried about <- logically linked
        USE_FALLBACK_LOADER = use_fallback_loader.checked;
        update_url_params();
    });
}

// ignore keyboard layout
function attach_keyboard_ui(presentation: Presentation): void {
    // according to KeyboardEvent.code on: https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/code/code_values
    const prev_keys = [
        "ArrowLeft",
        "ArrowDown",
        "PageDown",
        "Backspace",
    ];
    const next_keys = [
        "ArrowRight",
        "ArrowUp",
        "PageUp",
        "Enter",
        "Space",
    ];
    const fullscreen_keys = [
        "KeyF",
    ];

    document.addEventListener("keydown", (e: KeyboardEvent) => {
        if (e.repeat)
            return;
        if (prev_keys.includes(e.code))
            presentation.play_previous_section();
        else if (next_keys.includes(e.code))
            presentation.play_next_section();
        else if (fullscreen_keys.includes(e.code))
            presentation.toggle_fullscreen();
    });
}

document.body.onload = () => {
    load_url_params();
    let presentation = create_presentation();
    attach_ui(presentation);
    attach_keyboard_ui(presentation);
}
