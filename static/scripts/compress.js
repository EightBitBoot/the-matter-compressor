// TODO(Adin): Remove all logging in production

function updatePage() {
    $.get("/compress", function(data) {
        console.log("updatePage: " + data.is_compressing + ", " + data.num_compressions)
        if(data.is_compressing) {
            $("#compressButton").prop("disabled", true);
        }
        else {
            $("#compressButton").prop("disabled", false);
        }

        $("#times_compressed").html("Compressed " + data.num_compressions + " Times");
    }, "json");
}

function compress() {
    $.post("/compress", null, "json");
    updatePage();
}

eventSource = new EventSource("/events");
eventSource.addEventListener("keep_alive", function(event) {
    console.log(event);
});

eventSource.addEventListener("compress", function(event) {
    console.log(event);
    updatePage();
});

eventSource.onerror = function() {
    console.log("EventSource failed.");
};

window.onload = function() {
    updatePage();
}