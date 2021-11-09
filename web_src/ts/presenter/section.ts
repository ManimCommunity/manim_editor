export type SectionJson = {
    type: string;
    name: string;
    in_project_id: number;
    first_animation: number;
    after_last_animation: number;
    video: string;
};

export enum SectionType {
    NORMAL,
    LOOP,
    SKIP,
    COMPLETE_LOOP
}

export function get_section_type(str: string): SectionType {
    switch (str) {
        case "presentation.normal": return SectionType.NORMAL;
        case "presentation.loop": return SectionType.LOOP;
        case "presentation.skip": return SectionType.SKIP;
        case "presentation.complete_loop": return SectionType.COMPLETE_LOOP;
        default:
            console.error(`Unsupported section type '${str}'`);
            return SectionType.NORMAL;
    }
}

export abstract class Section {
    protected type: SectionType;
    protected name: string;
    protected id: number;
    protected video: string;

    // when section starts and ends
    // -1 -> hasn't ended/started yet
    protected start_time_stamp: number = -1;
    protected end_time_stamp: number = -1;

    public constructor(section: SectionJson, video: string) {
        this.type = get_section_type(section.type);
        this.name = section.name;
        this.id = section.in_project_id;
        // custom address from Flask
        this.video = video;
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
    // in seconds rounded to one decimal
    public get_sec_duration(): number {
        return Math.round(this.get_duration() / 100) / 10;
    }

    public get_type(): SectionType { return this.type; }
    public get_name(): string { return this.name; }
    public get_id(): number { return this.id; }
    public abstract get_src_url(): string;
}
