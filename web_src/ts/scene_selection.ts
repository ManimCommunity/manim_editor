import { send_json, flash, spin_button } from "./utils";

// set click callbacks
function attach_check_boxes(): void {
    let scenes = document.getElementsByClassName("scene-select") as HTMLCollectionOf<HTMLTableRowElement>;
    for (let scene of scenes) {
        let scene_check_box = scene.getElementsByClassName("scene-check-box")[0] as HTMLInputElement;
        scene_check_box.addEventListener("click", update_button);
    }
}

// activate button when at least one scene is selected
// has to be executed every time the check boxes get clicked
function update_button(): void {
    let check_boxes = document.getElementsByClassName("scene-check-box") as HTMLCollectionOf<HTMLInputElement>;
    let button = document.getElementById("confirm-button") as HTMLButtonElement;
    for (let check_box of check_boxes) {
        if (check_box.checked) {
            button.disabled = false;
            return;
        }
    }
    button.disabled = true;
}

// return list containing at index i the priority of the scene with priority i
// return empty list if priority used twice
function get_scene_priorities(): number[] {
    let scene_priorities = document.getElementsByClassName("scene-priority") as HTMLCollectionOf<HTMLSelectElement>;
    let priorities: number[] = [];
    // used to check if priority is used twice
    let used: boolean[] = Array(scene_priorities.length).fill(false);
    for (let i = 0; i < scene_priorities.length; ++i) {
        let priority = parseInt(scene_priorities[i].value);
        if (used[priority]) {
            flash(`The priority ${priority} can't be used twice.`, "danger");
            return [];
        }
        used[priority] = true;
        priorities.push(priority);
    }
    return priorities;
}

// return list of ids of selected scenes in order of their priority
function get_selected_scene_ids(): number[] {
    // used as lookup table
    let priorities = get_scene_priorities();
    if (!priorities.length)
        return [];

    let check_boxes = document.getElementsByClassName("scene-check-box") as HTMLCollectionOf<HTMLInputElement>;
    // list of selected sections for each scene in order of priority
    // -1 means not selected
    let selected_scene_ids: number[] = [];
    for (let i = 0; i < check_boxes.length; ++i)
        selected_scene_ids.push(-1);
    // go through scenes
    for (let i = 0; i < check_boxes.length; ++i)
        if (check_boxes[i].checked)
            // resolve priority
            selected_scene_ids[priorities[i]] = i;

    // filter out unselected -1
    let scene_ids: number[] = [];
    for (let id of selected_scene_ids)
        if (id != -1)
            scene_ids.push(id);

    // log order of scenes used
    let scene_log = "Used scene order: ";
    for (let scene_id of scene_ids)
        scene_log += `${scene_id} `;
    console.log(scene_log);
    return scene_ids;
}

function attach_button(): void {
    let button = document.getElementById("confirm-button") as HTMLButtonElement;
    let target = button.dataset.target as string;
    let project_name = button.dataset.project_name as string;
    let success_url = button.dataset.success_url as string;
    button.addEventListener("click", () => {
        let scene_ids = get_selected_scene_ids();
        // show flashes
        window.scrollTo(0, 0);
        // valid scene and priority selection?
        if (scene_ids.length) {
            flash("The project is being populated, this might take a few minutes. Open the terminal for more info.", "info");
            spin_button(button);
            let payload = {
                "name": project_name,
                "scene_ids": scene_ids,
            };
            send_json(target as string, payload, () => {
                // redirect at success
                window.location.href = success_url;
            }, () => {
                // failure
                flash(`The editor unexpectedly failed to populate the project '${project_name}'. For more information see the console log. Please consider opening an Issue on GitHub if this problem persists.`, "danger");
            });
        }
    });
}

document.body.onload = () => {
    attach_check_boxes();
    attach_button();
    // first update is for when the browser remembered some selections but the button stays inactive
    update_button();
};
