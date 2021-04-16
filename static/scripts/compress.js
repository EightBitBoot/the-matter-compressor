// TODO(Adin): Remove all logging in production
// TODO(Adin): Remove keep_alive event callback

// Previous compression state before updaatePage()
var previousCompressionState = false;
var eventSource;

function updatePage(fromMessage) {
    $.get("/compress", function(data) {
        console.log("updatePage: " + data.is_compressing + ", " + data.num_compressions)

        disableButton = false;
        if(data.is_compressing) {
            disableButton = true;
            $("#compressionMessage").html("Compression in progress");
        }
        else if(!data.can_compress) {
            disableButton = true;
            $("#compressionMessage").html("You already compressed the movie");
        }
        $("#compressButton").prop("disabled", disableButton);

        $("#timesCompressed").html("Compressed " + data.num_compressions + (data.num_compressions == 1 ? " Time" : " Times"));

        if(fromMessage && previousCompressionState) {
            // Refresh if compression is done
            location.reload();
        }

        previousCompressionState = data.is_compressing;
    }, "json");
}

function compress() {
    $.post("/compress", null, "json");
}

function initEventSource() {
    console.log("initEventSource()");
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

function onVisibilityChange() {
    if(document.visibilityState == "visible" && eventSource == null) {
        initEventSource()
    }
    else if(eventSource != null) {
        eventSource.close();
        eventSource = null;
    }

}

function initFingerprintAndUpdate() {
    // Initialize an agent at application startup.
    const fpPromise = FingerprintJS.load();

    // Get the visitor identifier when you need it.
    fpPromise
        .then(fp => fp.get())
        .then(result => {
            // This is the visitor identifier:
            const browser_fingerprint = result.visitorId;
            if(!document.cookie.includes("browser_fingerprint")) {
                console.log("browser_fingerprint=" + browser_fingerprint);
                document.cookie = "browser_fingerprint=" + browser_fingerprint + ";SameSite=strict";
            }

            updatePage(false);
    });
}

window.onload = function() {
    document.addEventListener("visibilitychange", onVisibilityChange);

    initEventSource();
    initFingerprintAndUpdate();
    // updatePage(false);  // This is called in initFingerprintAndUpdate() instead
}