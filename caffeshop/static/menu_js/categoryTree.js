function catecory_tree(clicked_id)
{
    var classNam = clicked_id + "1";
    const allCats = document.getElementsByClassName("cat");
    const thisCats = document.getElementsByClassName(classNam);
    for (item of allCats) {
      item.classList.remove("Active1");
    }
    for (var index=0;index < thisCats.length;index++) {
      thisCats[index].classList.add("Active1");
    }
}