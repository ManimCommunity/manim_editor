import { Presentation } from "../presenter/presentation";
import { SectionJson, Section, Slide } from "../presenter/section";
import { FallbackSection } from "./fallback_section";

// no buffering, only change src of video
export class FallbackPresentation extends Presentation {
    public override create_section(section_json: SectionJson, slide: Slide): Section {
        return new FallbackSection(section_json, slide);
    }
}
