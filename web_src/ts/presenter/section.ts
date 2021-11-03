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

    public get_type(): SectionType { return this.type; }
    public get_name(): string { return this.name; }
    public get_id(): number { return this.id; }
    public abstract get_src_url(): string;
}
