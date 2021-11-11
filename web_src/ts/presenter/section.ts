export type SectionJson = {
    type: string;
    name: string;
    in_project_id: number;
    first_animation: number;
    after_last_animation: number;
    video: string;
    sub_sections: number;
};

export enum SectionType {
    NORMAL,
    LOOP,
    SKIP,
    COMPLETE_LOOP
}

export function get_section_type(str: string): SectionType {
    switch (str) {
        case "normal": return SectionType.NORMAL;
        case "loop": return SectionType.LOOP;
        case "skip": return SectionType.SKIP;
        case "complete_loop": return SectionType.COMPLETE_LOOP;
        default:
            console.error(`Unsupported section type '${str}'`);
            return SectionType.NORMAL;
    }
}

export abstract class Section {
    protected type: SectionType;
    protected name: string;
    protected id: number;
    // custom address from Flask
    protected video: string;
    protected sub_sections: number;

    // null when sub section
    protected timeline_element: HTMLDivElement | null;
    protected timeline_indicator: HTMLElement | null;
    protected timeline_time_stamp: HTMLDivElement | null;

    // when section starts and ends
    // -1 -> hasn't ended/started yet
    protected start_time_stamp: number = -1;
    protected end_time_stamp: number = -1;

    public constructor(section: SectionJson, video: string) {
        this.type = get_section_type(section.type);
        this.name = section.name;
        this.id = section.in_project_id;
        this.video = video;
        this.sub_sections = section.sub_sections;

        this.timeline_element = document.getElementById(`timeline-element-${this.id}`) as HTMLDivElement | null;
        this.timeline_indicator = document.getElementById(`timeline-indicator-${this.id}`) as HTMLDivElement | null;
        this.timeline_time_stamp = document.getElementById(`timeline-time-stamp-${this.id}`) as HTMLDivElement | null;
    }

    public cache(on_cached: () => void): void {
        let request = new XMLHttpRequest();
        request.onload = () => {
            if (request.status == 200 || request.status == 206) {
                console.log(`Cached section '${this.name}'`)
                on_cached();
            }
            else {
                console.error(`Section '${this.name}' failed to be cached with status ${request.status}`);
                // another attempt in 10 sec
                window.setTimeout(() => {
                    this.cache(on_cached);
                }, 10000);
            }
        };
        request.onerror = () => {
            console.error(`Section '${this.name}' failed to be cached`);
            // another attempt in 10 sec
            window.setTimeout(() => {
                this.cache(on_cached);
            }, 10000);
        };
        request.open("GET", this.video, true);
        request.send();
    }

    public attach_timeline_click(callback: { (): void; }): void {
        if (this.timeline_element == null || this.timeline_time_stamp == null || this.timeline_indicator == null) {
            console.error(`Trying to add callback to sub section '${this.name}'.`);
            return;
        }
        this.timeline_element.addEventListener("click", callback);
    }
    public add_timeline_selection(): void {
        if (this.timeline_element == null || this.timeline_time_stamp == null || this.timeline_indicator == null) {
            console.error(`Trying to add timeline selection to sub section '${this.name}'.`);
            return;
        }
        // update indicator
        this.timeline_indicator.innerHTML = `<i class="timeline-indicators bi-circle-fill" role="img"></i>`;
        // add border
        this.timeline_element.classList.add("border-dark");
        // scroll
        // TODO: sometimes doesn't work on Chromium
        this.timeline_element.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
    public remove_timeline_selection(): void {
        if (this.timeline_element == null || this.timeline_time_stamp == null || this.timeline_indicator == null) {
            console.error(`Trying to remove timeline selection to sub section '${this.name}'.`);
            return;
        }
        // update time stamp of previous section
        this.timeline_time_stamp.innerText = `${this.get_sec_duration()} s`;
        // update indicator
        this.timeline_indicator.innerHTML = `<i class="timeline-indicators bi-check-circle" role="img"></i>`;
        // remove border
        this.timeline_element.classList.remove("border-dark");
    }

    public start_timer(): void {
        // console.error(`Starting section '${this.name}'`);
        this.start_time_stamp = performance.now();
        this.end_time_stamp = -1;
    }
    public stop_timer(): void {
        // console.error(`Stopping section '${this.name}'`);
        // prevent attempting to stop not started section
        if (this.end_time_stamp == -1 && this.start_time_stamp != -1)
            this.end_time_stamp = performance.now();
    }
    // in milliseconds
    public get_duration(): number {
        if (this.end_time_stamp == -1) {
            console.error(`Trying to get duration of section '${this.name}', which hasn't been stopped yet.`);
        }
        return this.end_time_stamp - this.start_time_stamp;
    }
    // in seconds rounded
    public get_sec_duration(): number {
        return Math.round(this.get_duration() / 1000);
    }

    public is_sub_section(): boolean {
        return this.sub_sections == -1;
    }

    public get_type(): SectionType { return this.type; }
    public get_name(): string { return this.name; }
    public get_id(): number { return this.id; }
    public abstract get_src_url(): string;
}
