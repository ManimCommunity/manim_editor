import { } from "./utils";

function set_scene_status(scene: HTMLTableRowElement, status: boolean): void {
    let scene_check_box = scene.getElementsByClassName("scene-check-box")[0] as HTMLInputElement;
    scene_check_box.checked = status;
    // apply to all sections
    let section_check_boxes = scene.getElementsByClassName("section-check-box") as HTMLCollectionOf<HTMLInputElement>;
    for (let section of section_check_boxes)
        section.checked = status;
}

// check if entire scene got turned on or off
function update_scene(scene: HTMLTableRowElement): void {
    let section_check_boxes = scene.getElementsByClassName("section-check-box") as HTMLCollectionOf<HTMLInputElement>;
    let new_status = section_check_boxes[0].checked;
    // check if all sections have same status
    for (let i = 1; i < section_check_boxes.length; ++i)
        if (section_check_boxes[i].checked != new_status)
            return;
    set_scene_status(scene, new_status);
}

function update_button(): void {
    let section_check_boxes = document.getElementsByClassName("section-check-box") as HTMLCollectionOf<HTMLInputElement>;
    let button = document.getElementById("confirm-button") as HTMLButtonElement;
    for (let section_check_box of section_check_boxes) {
        if (section_check_box.checked) {
            button.disabled = false;
            return;
        }
    }
    button.disabled = true;
}

// set click callbacks for scenes and sections
function watch_indices(): void {
    // scenes
    let scenes = document.getElementsByClassName("scene-select") as HTMLCollectionOf<HTMLTableRowElement>;
    for (let scene of scenes) {
        let scene_check_box = scene.getElementsByClassName("scene-check-box")[0] as HTMLInputElement;
        scene_check_box.addEventListener("click", () => {
            set_scene_status(scene, scene_check_box.checked);
            update_button();
        });
        // sections
        let sections = scene.getElementsByClassName("section-select") as HTMLCollectionOf<HTMLTableRowElement>;
        for (let section of sections) {
            let section_check_box = section.getElementsByClassName("section-check-box")[0] as HTMLInputElement;
            section_check_box.addEventListener("click", () => {
                update_scene(scene);
                update_button();
            })
        }
    }
}

document.body.onload = () => {
    watch_indices();
};
