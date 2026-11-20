const textarea = document.querySelector('textarea')
const addBtn = document.getElementById('addBtn')
const projectContainer = document.querySelector('.projectContainer')

//console.log(textarea.innerHTML)

let todoList = [] 

function init() {
    if(!localStorage.getItem('todos')){ return }
    todoList = JSON.parse(localStorage.getItem('todos')).todoList
    updateUI()
}
init()

function addProject() {
    const todo = textarea.value

    if(!todo){
        return;
    }

    console.log('Added todo: ', todo);
    todoList.push(todo)
    textarea.value = '' // resets to empty
    updateUI()
}

function editProject(index) {
    textarea.value = todoList[index]
    todoList = todoList.filter((element, elementIndex) => {
        if(index === elementIndex){ return false }
        return true
    })
    updateUI()
}

function deleteProject(index) {
    todoList = todoList.filter((element, elementIndex) => {
        if(index === elementIndex){ return false }
        return true
    })
    updateUI()
}


function updateUI() {
    let newInnerHTML = ''

    todoList.forEach((todoElement, todoIndex) => {
            newInnerHTML +=`
            <div class ="project">
                <p>${todoElement}</p>
                <div class="btnContainer">
                    <button class="iconBtn" onclick="editProject(${todoIndex})">
                        <i class="fa-solid fa-pencil"></i>
                    </button>
                    <button class="iconBtn" onclick="deleteProject(${todoIndex})">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </div>
            </div>
            `
        })

        projectContainer.innerHTML = newInnerHTML

        // save data to local storage
        localStorage.setItem('todos', JSON.stringify({ todoList }))
}

addBtn.addEventListener('click', addProject)
