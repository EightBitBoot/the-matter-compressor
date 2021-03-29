// TODO(Adin): Remove all logging in production

function compressionDoneCallback(data) {
    console.log("Compression success: " + data.success);

    if(data.success) {
        $("#compressButton").prop("disabled", true);
    }
}

function compress() {
    $.post("/compress", compressionDoneCallback, "json");
}

function onLoad() {
    $.get("/compress", function(data) {
        $("#times_compressed").html("Compressed " + data.num_compressions + " Times");

        if(data.is_compressing) {
            $("#compressButton").prop("disabled", true);
        }
    }, "json");
}

onLoad();