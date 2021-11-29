import {h, text, app} from "https://cdn.skypack.dev/hyperapp"

app({
  view: () => h("main", {}, [
    h("div", {class: "person"}, [
      h("p", {}, text("Hello world")),
    ]),
  ]),
  node: document.getElementById("app"),
})