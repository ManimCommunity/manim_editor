import { Section } from "../presenter/section";

export class FallbackSection extends Section {
    // use default video fetcher with no buffering
    public override get_src_url(): string {
        return this.video;
    }
}

