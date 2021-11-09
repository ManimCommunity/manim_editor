import { spin_button, get_json } from "../utils";
import { Section, SectionJson, SectionType } from "./section";

export abstract class Presentation {
    // using two video elements for smooth transitions
    private video0: HTMLVideoElement;
    private video1: HTMLVideoElement;
    private videos_div: HTMLDivElement;

    private timeline_sections: HTMLCollectionOf<HTMLDivElement>;
    private timeline_indicators: HTMLCollectionOf<HTMLElement>;
    private timeline_time_stamps: HTMLCollectionOf<HTMLDivElement>;

    private pause_button: HTMLButtonElement;

    private normal_legend: HTMLTableRowElement;
    private skip_legend: HTMLTableRowElement;
    private loop_legend: HTMLTableRowElement;
    private complete_loop_legend: HTMLTableRowElement;

    // switch between play and pause
    private button_should_pause = true;

    private go_back_time: number;
    private cache_batch_size: number;
    // gets flipped when displaying first video
    private current_video = 1;

    protected sections: Section[] = [];
    protected current_section = -1;
    // used for restarting loops
    // <- has to be done to allow complete loops
    // also used for setting time stamps
    // most of the time same as current_section, only different when video element has to be touched
    private previous_section = -1;
    // used for complete loops
    private next_section = 0;

    public constructor(go_back_time: number, cache_batch_size: number) {
        this.go_back_time = go_back_time;
        this.cache_batch_size = cache_batch_size;

        this.video0 = document.getElementById("video0") as HTMLVideoElement;
        this.video1 = document.getElementById("video1") as HTMLVideoElement;
        this.videos_div = document.getElementById("videos-div") as HTMLDivElement;
        this.timeline_sections = document.getElementsByClassName("timeline-element") as HTMLCollectionOf<HTMLDivElement>;
        this.timeline_indicators = document.getElementsByClassName("timeline-indicator") as HTMLCollectionOf<HTMLDivElement>;
        this.timeline_time_stamps = document.getElementsByClassName("timeline-time-stamp") as HTMLCollectionOf<HTMLDivElement>;
        this.pause_button = document.getElementById("pause") as HTMLButtonElement;
        this.normal_legend = document.getElementById("normal-legend") as HTMLTableRowElement;
        this.skip_legend = document.getElementById("skip-legend") as HTMLTableRowElement;
        this.loop_legend = document.getElementById("loop-legend") as HTMLTableRowElement;
        this.complete_loop_legend = document.getElementById("complete-loop-legend") as HTMLTableRowElement;

        // load_sections
        let project_file = this.videos_div.dataset.project_file as string;
        get_json(project_file, (sections: SectionJson[]) => {
            // construct sections from json response
            for (let i = 0; i < sections.length; ++i) {
                // custom Flask url
                let video = this.timeline_sections[i].dataset.video as string;
                this.add_section(sections[i], video);
            }
            console.log(`All ${sections.length} sections have been parsed successfully.`)

            this.attach_timeline();
            this.attach_buttons();
            // start the action
            this.play_section(0);
        });
    }

    // to be used when section has ended
    private set_time_stamp(): void {
        if (this.previous_section != -1)
            this.sections[this.previous_section].stop_timer();
        this.sections[this.current_section].start_timer();
    }

    // update currently playing video in html video element
    private update_video(): void {
        this.set_button_pause();
        // correct section already current
        if (this.current_section == this.previous_section) {
            // restart video
            this.get_current_video().currentTime = 0;
            this.get_current_video().play();
            return;
        }
        // swap videos
        let last_element = this.get_current_video();
        this.current_video = this.current_video == 0 ? 1 : 0;
        let next_element = this.get_current_video();

        // double buffering: setup new video
        next_element.src = this.sections[this.current_section].get_src_url();
        next_element.style.visibility = "visible";

        // set callback for when video has ended
        switch (this.sections[this.current_section].get_type()) {
            case SectionType.SKIP:
                next_element.onended = (_) => {
                    // immediately go to next section without user input
                    ++this.current_section;
                    this.next_section = this.current_section;
                    this.set_time_stamp();
                    this.update_video();
                }
                break;
            case SectionType.LOOP:
                next_element.onended = (_) => {
                    // restart from beginning
                    // section ends -> don't set timestamp
                    this.update_video();
                }
                break;
            case SectionType.COMPLETE_LOOP:
                next_element.onended = (_) => {
                    // when next section has changed, go to next one
                    // otherwise restart
                    this.current_section = this.next_section;
                    this.set_time_stamp();
                    this.update_video();
                }
                break;
            // SectionType.NORMAL
            default:
                // do nothing <- wait for user input
                next_element.onended = (_) => { }
                break;
        }

        console.log(`Playing section '${this.sections[this.current_section].get_name()}'`)
        // hide old video once new one plays
        next_element.play().then(() => {
            // pause old video to not call onended callback again when that video ends in background
            last_element.pause();
            last_element.style.visibility = "hidden";
        });

        this.update_timeline()
        this.update_source();

        // everything done -> section has changed
        this.previous_section = this.current_section;
    }

    // skip_complete_loop can be used in the timeline or as a forced continue
    public play_section(section: number, skip_complete_loop = false): void {
        // out of bounds checking
        if (section < 0)
            section = 0;
        else if (section >= this.sections.length) {
            // skip to end of current section
            this.get_current_video().currentTime = this.get_current_video().duration;
            return;
        }

        console.log(`Switching to section '${this.sections[section].get_name()}'`);
        if (this.current_section != -1 &&
            this.sections[this.current_section].get_type() == SectionType.COMPLETE_LOOP &&
            !skip_complete_loop) {
            // if current section is complete loop, wait until it finishes
            this.next_section = section;
        } else {
            // instantly switch the video
            this.next_section = section;
            this.current_section = section;
            this.set_time_stamp();
            this.update_video();
        }
    }

    public play_next_section(): void {
        this.play_section(this.current_section + 1, false);
    }
    public play_next_section_forced(): void {
        this.play_section(this.current_section + 1, true);
    }
    public restart_current_section(): void {
        this.play_section(this.current_section, true);
    }
    public play_previous_section(): void {
        // required to get an accurate duration readout
        this.sections[this.current_section].stop_timer();
        // either restart or go back
        if (this.go_back_time < 0 || this.sections[this.current_section].get_duration() < this.go_back_time) {
            this.play_previous_section_forced();
        }
        else
            this.restart_current_section();
    }
    public play_previous_section_forced(): void {
        // don't finish complete loops when going back
        this.play_section(this.current_section - 1, true);
    }

    public get_current_section(): number { return this.current_section; }

    private get_current_video(): HTMLVideoElement {
        if (this.current_video == 0)
            return this.video0;
        else
            return this.video1;
    }

    /////////////
    // caching //
    /////////////
    // asynchronous, recursive; downloads everything after offset in batches
    private cache_batch(offset: number, on_finished: { (): void; }): void {
        let finished = offset;
        // cache one whole batch
        for (let i = offset, len = Math.min(offset + this.cache_batch_size, this.sections.length); i < len; ++i)
            this.sections[i].cache(() => {
                ++finished;
                // all finished
                if (finished == this.sections.length) {
                    console.log(`Batch caching complete with offset ${offset}`)
                    console.log("Caching complete");
                    on_finished();
                }
                // start next batch
                else if (finished == offset + this.cache_batch_size) {
                    console.log(`Batch caching complete with offset ${offset}`)
                    this.cache_batch(finished, on_finished);
                }
            });
    }

    // asynchronous
    public cache(on_finished: { (): void; }): void {
        this.cache_batch(0, on_finished);
    }

    ////////////////
    // fullscreen //
    ////////////////
    public enter_fullscreen(): void {
        console.log("Entering fullscreen.");
        // conversion to any required because WebKit API not known to TypeScript
        if ((this.videos_div as any).requestFullscreen)
            this.videos_div.requestFullscreen();
        // safari
        else if ((this.videos_div as any).webkitRequestFullscreen)
            (this.videos_div as any).webkitRequestFullscreen();
    }

    public exit_fullscreen(): void {
        console.log("Exiting fullscreen.");
        if ((document as any).exitFullscreen)
            (document as any).exitFullscreen();
        // safari
        else if ((document as any).webkitExitFullscreen)
            (document as any).webkitExitFullscreen();
    }

    private fullscreen_status(): boolean {
        return (document as any).fullscreenElement != null ||
            (document as any).webkitFullscreenElement != null;
    }

    public toggle_fullscreen(): void {
        if (this.fullscreen_status())
            this.exit_fullscreen();
        else
            this.enter_fullscreen();
    }

    ////////////////////
    // user interface //
    ////////////////////
    private attach_timeline(): void {
        for (let i = 0; i < this.timeline_sections.length; ++i) {
            this.timeline_sections[i].addEventListener("click", () => {
                this.play_section(i, true);
            });
        }
    }

    private update_timeline(): void {
        // update time stamp in timeline of previous section
        if (this.previous_section != -1)
            this.timeline_time_stamps[this.previous_section].innerText = `${this.sections[this.previous_section].get_sec_duration()}sec`;

        // deselect old section in timeline, select current and scroll to
        if (this.previous_section != -1)
            this.timeline_indicators[this.previous_section].innerHTML = `<i class="timeline-indicators bi-check-circle" role="img"></i>`;
        this.timeline_indicators[this.current_section].innerHTML = `<i class="timeline-indicators bi-circle-fill" role="img"></i>`;
        // TODO: sometimes doesn't work on Chromium
        this.timeline_sections[this.current_section].scrollIntoView({ behavior: "smooth", block: "center" });

        // remove old type in legend and select current
        if (this.previous_section != -1)
            switch (this.sections[this.previous_section].get_type()) {
                case SectionType.NORMAL:
                    this.normal_legend.classList.remove("table-active");
                    break;
                case SectionType.SKIP:
                    this.skip_legend.classList.remove("table-active");
                    break;
                case SectionType.LOOP:
                    this.loop_legend.classList.remove("table-active");
                    break;
                case SectionType.COMPLETE_LOOP:
                    this.complete_loop_legend.classList.remove("table-active");
                    break;
            }
        switch (this.sections[this.current_section].get_type()) {
            case SectionType.NORMAL:
                this.normal_legend.classList.add("table-active");
                break;
            case SectionType.SKIP:
                this.skip_legend.classList.add("table-active");
                break;
            case SectionType.LOOP:
                this.loop_legend.classList.add("table-active");
                break;
            case SectionType.COMPLETE_LOOP:
                this.complete_loop_legend.classList.add("table-active");
                break;
        }
    }

    // update icon on button
    private set_button_play(): void {
        this.button_should_pause = false;
        this.pause_button.innerHTML = '<i class="bi-play"></i>';
    }
    private set_button_pause(): void {
        this.button_should_pause = true;
        this.pause_button.innerHTML = '<i class="bi-pause"></i>';
    }

    public pause(): void {
        console.log("Stopped.");
        this.get_current_video().pause();
        this.set_button_play();
    }
    public play(): void {
        console.log("Started.");
        this.get_current_video().play();
        this.set_button_pause();
    }
    public toggle_pause(): void {
        if (this.button_should_pause)
            this.pause();
        else
            this.play();
    }

    public attach_buttons(): void {
        let previous = document.getElementById("previous-section") as HTMLButtonElement;
        let restart = document.getElementById("restart-section") as HTMLButtonElement;
        let next = document.getElementById("next-section") as HTMLButtonElement;
        let pause = document.getElementById("pause") as HTMLButtonElement;
        let fullscreen = document.getElementById("fullscreen") as HTMLButtonElement;
        let cache = document.getElementById("cache") as HTMLButtonElement;

        // add callbacks
        previous.addEventListener("click", this.play_previous_section.bind(this));
        restart.addEventListener("click", this.restart_current_section.bind(this));
        next.addEventListener("click", this.play_next_section.bind(this));
        pause.addEventListener("click", this.toggle_pause.bind(this));
        fullscreen.addEventListener("click", this.enter_fullscreen.bind(this));
        cache.addEventListener("click", () => {
            spin_button(cache);
            this.cache(() => {
                cache.remove();
            });
        });
        this.videos_div.addEventListener("touchstart", this.play_next_section.bind(this));
    }

    ////////////////////////////////
    // to be defined by inheritor //
    ////////////////////////////////
    protected abstract add_section(section: SectionJson, video: string): void;

    // called after section changed
    // to be overwritten if required
    protected update_source(): void { }
};
