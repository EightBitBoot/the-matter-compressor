function compress() {
    $.post("/compress", function(data) {
        console.log(data.success);
    }, "json");
}