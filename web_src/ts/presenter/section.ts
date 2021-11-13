export type SlideJson = {
    sections: SectionJson[];
};

export type SectionJson = {
    type: string;
    name: string;
    in_project_id: number;
    first_animation: number;
    after_last_animation: number;
    video: string;
    parent_id: number;
    is_sub_section: boolean;
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

// contains one section with 0 or more sub sections
export class Slide {
    private sections: Section[];
    // is id of first section
    private id: number;

    protected timeline_element: HTMLDivElement;
    protected timeline_time_stamp: HTMLDivElement;
    protected timeline_indicator: HTMLElement;

    public constructor(slide_json: SlideJson, create_section: { (section_json: SectionJson, slide: Slide): Section; }) {
        this.sections = [];
        for (let section_json of slide_json.sections) {
            this.sections.push(create_section(section_json, this));
        }
        this.id = this.sections[0].get_id();

        this.timeline_element = document.getElementById(`timeline-element-${this.id}`) as HTMLDivElement;
        this.timeline_indicator = document.getElementById(`timeline-indicator-${this.id}`) as HTMLDivElement;
        this.timeline_time_stamp = document.getElementById(`timeline-time-stamp-${this.id}`) as HTMLDivElement;
        console.log(`Parsed slide #${this.id} with ${this.sections.length} sections.`);
    }

    public get_sections(): Section[] { return this.sections; }
    public get_id(): number { return this.id; }

    // sum of time spent in sections in milliseconds
    // unstopped sections don't get counted
    public get_duration(): number {
        let sum: number = 0;
        for (let section of this.sections) {
            if (section.has_stopped())
                sum += section.get_duration();
        }
        return sum;
    }
    // in seconds rounded
    public get_sec_duration(): number {
        return Math.round(this.get_duration() / 1000);
    }

    public attach_timeline_click(callback: { (): void; }): void {
        this.timeline_element.addEventListener("click", callback);
    }

    public add_timeline_selection(): void {
        // update indicator
        this.timeline_indicator.innerHTML = `<i class="timeline-indicators bi-circle-fill" role="img"></i>`;
        // add border
        this.timeline_element.classList.add("border-dark");
        // scroll
        // TODO: sometimes doesn't work on Chrome
        this.timeline_element.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }

    public remove_timeline_selection(): void {
        // update time stamp of previous section
        this.timeline_time_stamp.innerText = `${this.get_sec_duration()} s`;
        // update indicator
        this.timeline_indicator.innerHTML = `<i class="timeline-indicators bi-check-circle" role="img"></i>`;
        // remove border
        this.timeline_element.classList.remove("border-dark");
    }
}

export abstract class Section {
    protected type: SectionType;
    protected name: string;
    protected id: number;
    // custom address from Flask
    protected video: string;
    protected is_sub_section: boolean;

    protected parent_slide: Slide;

    // when section starts and ends
    // -1 -> hasn't ended/started yet
    protected start_time_stamp: number = -1;
    protected end_time_stamp: number = -1;

    public constructor(section_json: SectionJson, parent_slide: Slide) {
        this.type = get_section_type(section_json.type);
        this.name = section_json.name;
        this.id = section_json.in_project_id;
        this.is_sub_section = section_json.is_sub_section;

        this.parent_slide = parent_slide;

        // custom Flask url
        let section_urls = document.getElementsByClassName("section-urls") as HTMLCollectionOf<HTMLDivElement>;
        this.video = section_urls[this.id].dataset.video as string;
        console.log(`Parsed section #'${this.id}'`);
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

    public has_started(): boolean {
        return this.start_time_stamp != -1;
    }
    public has_stopped(): boolean {
        return this.end_time_stamp != -1;
    }
    public start_timer(): void {
        this.start_time_stamp = performance.now();
        this.end_time_stamp = -1;
    }
    public stop_timer(): void {
        // prevent attempting to stop not started section
        if (!this.has_stopped() && this.has_started())
            this.end_time_stamp = performance.now();
    }
    // in milliseconds
    public get_duration(): number {
        if (!this.has_stopped())
            console.error(`Trying to get duration of section '${this.name}', which hasn't been stopped yet.`);
        return this.end_time_stamp - this.start_time_stamp;
    }
    // in seconds rounded
    public get_sec_duration(): number {
        return Math.round(this.get_duration() / 1000);
    }

    public get_is_sub_section(): boolean { return this.is_sub_section; }
    public get_type(): SectionType { return this.type; }
    public get_name(): string { return this.name; }
    public get_id(): number { return this.id; }
    public get_parent_slide(): Slide { return this.parent_slide; }

    // to be defined by inheritor
    public abstract get_src_url(): string;
}
