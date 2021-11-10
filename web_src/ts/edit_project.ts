import { spin_button } from "./utils";
import { Presentation } from "./presenter/presentation";
import { BufferPresentation } from "./buffer_presenter/buffer_presentation";
import { FallbackPresentation } from "./fallback_presenter/fallback_presentation";
import { send_json, flash } from "./utils";
import * as Bowser from "bowser";

// used to load and update player settings
// NOTE: in milliseconds rather than seconds as inputted by the user
let GO_BACK_TIME = 500;
let CACHE_BATCH_SIZE = 3;
let PAST_SECTIONS_TO_BUFFER = 10;
let FUTURE_SECTIONS_TO_BUFFER = 20;
let USE_FALLBACK_LOADER = false;
let url_search_params = new URLSearchParams(location.search);

function load_url_params(): void {
    if (url_search_params.has("go_back_time"))
        GO_BACK_TIME = Number(url_search_params.get("go_back_time"));
    if (url_search_params.has("cache_batch_size"))
        CACHE_BATCH_SIZE = Number(url_search_params.get("cache_batch_size"));
    if (url_search_params.has("past_sections_to_buffer"))
        PAST_SECTIONS_TO_BUFFER = Number(url_search_params.get("past_sections_to_buffer"));
    if (url_search_params.has("future_sections_to_buffer"))
        FUTURE_SECTIONS_TO_BUFFER = Number(url_search_params.get("future_sections_to_buffer"));
    if (url_search_params.has("use_fallback_loader"))
        USE_FALLBACK_LOADER = url_search_params.get("use_fallback_loader") === "true";
}

// update url parameter and reload page
function update_url_params(): void {
    url_search_params.set("go_back_time", GO_BACK_TIME.toString());
    url_search_params.set("cache_batch_size", CACHE_BATCH_SIZE.toString());
    url_search_params.set("past_sections_to_buffer", FUTURE_SECTIONS_TO_BUFFER.toString());
    url_search_params.set("future_sections_to_buffer", PAST_SECTIONS_TO_BUFFER.toString());
    url_search_params.set("use_fallback_loader", USE_FALLBACK_LOADER.toString());

    window.history.replaceState({}, "", `${location.pathname}?${url_search_params.toString()}`);
    location.reload();
}

// remove url parameter and reload page
function discard_url_params(): void {
    window.history.replaceState({}, "", `${location.pathname}`);
    location.reload();
}

function create_presentation(): Presentation {
    if (USE_FALLBACK_LOADER) {
        console.log(`Using FallbackPresentation with a cache batch size of ${CACHE_BATCH_SIZE}.`);
        return new FallbackPresentation(GO_BACK_TIME, CACHE_BATCH_SIZE);
    }
    else {
        console.log(`Using BufferPresentation with ${FUTURE_SECTIONS_TO_BUFFER} sections to auto load, ${PAST_SECTIONS_TO_BUFFER} sections to keep and a cache batch size of ${CACHE_BATCH_SIZE}.`);
        return new BufferPresentation(GO_BACK_TIME, CACHE_BATCH_SIZE, FUTURE_SECTIONS_TO_BUFFER, PAST_SECTIONS_TO_BUFFER);
    }
}

function attach_settings(): void {
    let go_back_time = document.getElementById("go-back-time") as HTMLInputElement;
    let cache_batch_size = document.getElementById("cache-batch-size") as HTMLInputElement;
    let past_sections_to_buffer = document.getElementById("past-sections-to-buffer") as HTMLInputElement;
    let future_sections_to_buffer = document.getElementById("future-sections-to-buffer") as HTMLInputElement;
    let use_fallback_loader = document.getElementById("fallback-loader-selected") as HTMLInputElement;
    let reset_settings = document.getElementById("reset-settings") as HTMLButtonElement;
    let update_settings = document.getElementById("update-settings") as HTMLButtonElement;

    go_back_time.value = Math.round(GO_BACK_TIME / 1000).toString();
    cache_batch_size.value = CACHE_BATCH_SIZE.toString();
    past_sections_to_buffer.value = PAST_SECTIONS_TO_BUFFER.toString();
    future_sections_to_buffer.value = FUTURE_SECTIONS_TO_BUFFER.toString();
    // automatically set use_buffer_loader
    use_fallback_loader.checked = USE_FALLBACK_LOADER;

    // set callback
    reset_settings.addEventListener("click", discard_url_params);
    update_settings.addEventListener("click", () => {
        // silently prevent invalid input
        // TODO: add error message
        if (!isNaN(parseInt(go_back_time.value)))
            GO_BACK_TIME = parseInt(go_back_time.value) * 1000;
        if (parseInt(cache_batch_size.value) > 0)
            CACHE_BATCH_SIZE = parseInt(cache_batch_size.value);
        if (parseInt(past_sections_to_buffer.value) > 0)
            PAST_SECTIONS_TO_BUFFER = parseInt(past_sections_to_buffer.value);
        if (parseInt(future_sections_to_buffer.value) > 0)
            FUTURE_SECTIONS_TO_BUFFER = parseInt(future_sections_to_buffer.value);
        // buffer-loader-selected doesn't have to be worried about <- logically linked
        USE_FALLBACK_LOADER = use_fallback_loader.checked;
        update_url_params();
    });
}

function attach_export(): void {
    let export_presentation = document.getElementById("export-presentation") as HTMLButtonElement | null;
    if (export_presentation !== null) {
        let target = export_presentation.dataset.target as string;
        let project_name = export_presentation.dataset.name as string;
        export_presentation.addEventListener("click", () => {
            // flash("The project is being exported as a presentation, this might take a few seconds. Open the terminal for more info.", "info");
            spin_button(export_presentation as HTMLButtonElement);
            send_json(target, { "name": project_name }, (response: any) => {
                if (response.success) {
                    export_presentation?.remove();
                    flash("The project has been exported, copy the project directory into a web server to serve it. More information can be found in the documentation.", "success");
                }
                else
                    flash(`The editor unexpectedly failed to export the project '${project_name}' as a presentation. For more information see the console log. Please consider opening an Issue on GitHub if this problem persists.`, "danger");
            });
        });
    }
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
    ];
    const pause_keys = [
        "Space",
    ];
    const fullscreen_keys = [
        "KeyF",
    ];
    const all_keys = prev_keys.concat(next_keys, pause_keys, fullscreen_keys);

    document.addEventListener("keydown", (e: KeyboardEvent) => {
        // prevent keys from scrolling page or clicking buttons
        if (all_keys.includes(e.code))
            e.preventDefault();

        // catch keys only once
        if (e.repeat)
            return;

        // run function in presentation
        if (prev_keys.includes(e.code) && (e.ctrlKey || e.metaKey))
            presentation.play_previous_section_forced();
        else if (prev_keys.includes(e.code))
            presentation.play_previous_section();

        else if (next_keys.includes(e.code) && (e.ctrlKey || e.metaKey))
            presentation.play_next_section_forced();
        else if (next_keys.includes(e.code))
            presentation.play_next_section();

        else if (pause_keys.includes(e.code))
            presentation.toggle_pause();

        else if (fullscreen_keys.includes(e.code))
            presentation.toggle_fullscreen();
    });
}

function check_browser(): void {
    const browser = Bowser.getParser(window.navigator.userAgent);
    // TODO: add better versions that have actually been tested
    const is_valid = browser.satisfies({
        firefox: ">80",
        chrome: ">80",
        edge: ">40",
    });
    if (!is_valid)
        flash("Your browser isn't officially supported. If you encounter any problems use a recent Version of Firefox, Chrome or Edge. Consider opening an Issue on GitHub to remove this warning if your browser works regardless.", "warning");
}

document.body.onload = () => {
    load_url_params();
    let presentation = create_presentation();
    attach_settings();
    attach_export();
    attach_keyboard_ui(presentation);
    check_browser();
}
