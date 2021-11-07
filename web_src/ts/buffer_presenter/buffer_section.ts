import { SectionJson, Section } from "../presenter/section";

export class BufferSection extends Section {
    private media_source: MediaSource = new MediaSource();
    private media_buffer: BufferSource | null = null;

    public constructor(section: SectionJson, video: string) {
        super(section, video);
        // when setting url to video element
        this.media_source.onsourceopen = (_) => {
            // check if MIME codec is supported
            let mime_codec = 'video/mp4; codecs="avc1.64002A"';
            if (!("MediaSource" in window) || !MediaSource.isTypeSupported(mime_codec)) {
                console.error("MediaSource or mime codec not supported");
                this.media_source.endOfStream();
                return;
            }

            // add source buffer to media source of this section
            let source_buffer = this.media_source.addSourceBuffer(mime_codec);

            // set callbacks
            source_buffer.onupdateend = (_) => {
                this.media_source.endOfStream();
            };
            source_buffer.onerror = (_) => {
                console.error("Failed to append buffer to source buffer:");
                console.error(this.media_source);
            };
            source_buffer.onabort = (_) => {
                console.error("Aborted source buffer:");
                console.error(this.media_source);
            };

            this.load(() => {
                if (this.media_buffer == null) {
                    source_buffer.abort();
                    return;
                }
                // success
                source_buffer.appendBuffer(this.media_buffer);
            }, () => {
                // failure
                source_buffer.abort();
            });
        }
    }

    public load(
        on_loaded: (() => void) | null = null,
        on_failed: (() => void) | null = null
    ): void {
        if (this.media_buffer !== null) {
            if (on_loaded !== null)
                on_loaded();
            return;
        }

        let request = new XMLHttpRequest();
        request.responseType = "arraybuffer";
        request.onload = () => {
            this.media_buffer = request.response;
            console.log(`Section '${this.name}' successfully loaded`);
            if (on_loaded !== null)
                on_loaded();
        };
        request.onerror = () => {
            console.error(`Section '${this.name}' failed to load`);
            if (on_failed !== null)
                on_failed();
        };
        request.open("GET", this.video, true);
        request.send();
    }

    public unload(): void {
        this.media_buffer = null;
    }

    // load from memory
    public override get_src_url(): string {
        return URL.createObjectURL(this.media_source);
    }
}
