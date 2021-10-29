# Manim Editor

## [Working Example](https://manimeditorproject.github.io/manim_editor/tutorial/)

Editor and Presenter for Manim Generated Content

https://manim-editor.readthedocs.io/en/latest/

Since the [Section API](https://github.com/ManimCommunity/manim/pull/2152) has been merged, the Manim Web Presenter (https://github.com/christopher-besch/manim_web_presenter) will have to be rewritten.
This editor will take that functionality and add some more: It will be something like a "Manim video editor", where you load your scenes and record your lovely voice.
(Here I'll reuse some of the presentation code, which is why these two functions, editing and presenting, will be implemented in the same repo.)
Then it will sync the voice with the video without any user input required; loops shall be looped, seamless transitions seamlessly transitioned and pauses paused(?)

My goal is for this repo to eventually become part of the ManimCommunity Organisation.
With such a tool, Manim can really rival something like PowerPoint.

If anyone would like to join forces, I'm happy to add them to the (hopefully intermediate) ManimEditorProject organisation.

# Build from Source

- clone repo: `git clone https://github.com/ManimEditorProject/manim_editor && cd manim_editor`
- install poetry dependencies: `poetry install`
- enter poetry shell: `poetry shell`
- install npm modules: `npm ci`
- compile web files: `npm run build_debug` or `npm run build_release`
- start editor: `manedit`
