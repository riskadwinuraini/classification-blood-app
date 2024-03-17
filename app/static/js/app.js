$(document).ready(function () {
    // Fungsi upload image ketika dipilih
    $("#upload-img").change(function (event) {
        var files = event.target.files;

        if (files && files.length > 0) {
            var file = files[0];
            var reader = new FileReader();

            reader.onload = function (e) {

                var base64data = reader.result;

                $.ajax({
                    url: "/tmp",
                    type: "POST",
                    data: { image: base64data },
                    contentType: "application/x-www-form-urlencoded",
                    success: function (data) {
                        $("#img-prev")
                            .attr(
                                "src",
                                "http://127.0.0.1:4000/static/temp/" +
                                    data.image_path
                                        .split("\\")
                                        .pop()
                                        .split("/")
                                        .pop()
                            )
                            .attr(
                                "data-trigger",
                                "data:image/png;base64," + base64data
                            );
                    },
                    error: function (err) {
                        console.log(err);
                    },
                });
            };

            reader.readAsDataURL(file);
        }
    });

    $("#btn-process").click(function (e) {
        e.preventDefault();

        var base64data = reader.result.split(",")[1];

        // $.ajax({
        //     url: "/classify",
        //     type: "POST",
        //     data: {
        //         image: $("#img-prev").attr("data-trigger"),
        //     },
        //     contentType: "application/x-www-form-urlencoded",
        //     success: function (data) {
        //         console.log(data);
        //     },
        //     error: function (err) {
        //         console.log(err);
        //     },
        // });
    });
});
