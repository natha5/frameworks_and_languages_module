import {h, text, app} from "https://cdn.skypack.dev/hyperapp"

app({
  view: () => h("main", {}, [
    h("div", {class: "person"}, [
      h("p", {}, text("Hello world")),

      h("section", {}, [
        h("input", { type: "text", oninput: NewValue, value }),
        h("button", { onclick: AddTodo }, text("Add new")),  
      ])
    ]),
  ]),
  node: document.getElementById("app"),
})