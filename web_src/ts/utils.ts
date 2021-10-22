export function select_file(id: string): void {
    let selector = document.getElementById(id) as HTMLInputElement;
    selector.addEventListener("change", (file) => {
        console.log(file);
    });
}
