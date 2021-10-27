import { Presentation } from "../presenter/presentation";
import { SectionJson } from "../presenter/section";
import { BufferSection } from "./buffer_section";

export class BufferPresentation extends Presentation {
    // when both 0, only current section will be buffered
    private future_sections_to_buffer;
    private past_sections_to_buffer;

    public constructor(cache_batch_size: number, past_sections_to_buffer: number, future_sections_to_buffer: number) {
        super(cache_batch_size);
        this.past_sections_to_buffer = past_sections_to_buffer;
        this.future_sections_to_buffer = future_sections_to_buffer;
    }

    // buffer past and future videos
    protected override update_source(): void {
        // load next sections
        for (let i = this.current_section + 1, len = Math.min(this.current_section + this.future_sections_to_buffer + 1, this.sections.length); i < len; ++i)
            (this.sections[i] as BufferSection).load();
        // unload previous sections
        for (let i = 0, len = this.current_section - this.past_sections_to_buffer; i < len; ++i)
            (this.sections[i] as BufferSection).unload();
    }

    protected override add_section(section: SectionJson, video: string): void {
        this.sections.push(new BufferSection(section, video));
    }
}
