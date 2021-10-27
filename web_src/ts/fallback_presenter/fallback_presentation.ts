import { Presentation } from "../presenter/presentation";
import { SectionJson } from "../presenter/section";
import { FallbackSection } from "./fallback_section";

// no buffering, only change src of video
export class FallbackPresentation extends Presentation {
    public override add_section(section: SectionJson): void {
        this.sections.push(new FallbackSection(section));
    }
}
