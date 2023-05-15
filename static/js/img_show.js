const input = document.querySelector("#input_imgs")
const output = document.querySelector("#output_imgs")
let imagesArray = []

input.addEventListener("change", () => {
    const files = input.files
    for (let i = 0; i < files.length; i++) {
        imagesArray.push(files[i])
    }
    displayImages()
})

function displayImages() {
    let images = ""
    imagesArray.forEach((image, index) => {
        images += `<div class="image">
                        <img src="${URL.createObjectURL(image)}" alt="image">
                        <span onclick="deleteImage(${index})">&times;</span>
                    </div>`
    })
    output.innerHTML = images

    // Update the file list with added or deleted images
    const newFileList = createFileList(imagesArray)
    input.files = newFileList
}

function deleteImage(index) {
    imagesArray.splice(index, 1)
    displayImages()
}

function createFileList(files) {
    // Creating a new filelist because a filelist object is read-only
    const dataTransfer = new DataTransfer()
    for (let i = 0; i < files.length; i++) {
        dataTransfer.items.add(files[i])
    }
    return dataTransfer.files
}


const input_del = document.querySelector("#del_imgs")
let imagesDelUrl = []

function deleteExistingImage(image_id, count) {
    // Remove image from html
    const element = document.getElementById(image_id);
    element.remove();

    imagesDelUrl.push(image_id)

    if (imagesDelUrl.length == count) {
        const element_section = document.getElementById("existing-imgs");
        element_section.remove();
    }
    
    // Send image ids to Django
    input_del.value = imagesDelUrl
}