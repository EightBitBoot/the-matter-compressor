// TODO(Adin): Remove all logging in production
// TODO(Adin): Remove keep_alive event callback

// Variable to store previous state of compression
// before updatePage has finished so that when the
// state goes from compressing to not compressing 
// the page can be refreshed
var wasCompressing = false;
var eventSource;

function updatePage(fromMessage) {
    $.get("/compress", function(data) {
        console.log("updatePage: " + data.is_compressing + ", " + data.num_compressions)
        if(data.is_compressing) {
            $("#compressButton").prop("disabled", true);
        }
        else {
            $("#compressButton").prop("disabled", false);
        }

        $("#times_compressed").html("Compressed " + data.num_compressions + " Times");

        if(fromMessage && wasCompressing) {
            // Refresh if compression is done
            location.reload();
        }

        wasCompressing = data.is_compressing;
    }, "json");
}

function compress() {
    $.post("/compress", null, "json");
    updatePage(false);
}

function onVisibilityChange() {
    if(document.visibilityState == "visible") {
        eventSource = new EventSource("/events");
        eventSource.addEventListener("keep_alive", function(event) {
            console.log(event);
        });

        eventSource.addEventListener("compress", function(event) {
            console.log(event);
            updatePage(true);
        });

        eventSource.onerror = function() {
            console.log("EventSource failed.");
        };
    }
    else if(eventSource != null) {
        eventSource.close();
    }

}

window.onload = function() {
    document.addEventListener("visibilitychange", onVisibilityChange);

    updatePage(false);
}