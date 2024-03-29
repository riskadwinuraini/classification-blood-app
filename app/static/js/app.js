$(document).ready(function () {
    var reader = new FileReader();
    // Fungsi upload image ketika dipilih
    $("#upload-img").change(function (event) {
        var files = event.target.files;

        if (files && files.length > 0) {
            var file = files[0];

            reader.onloadend = function (e) {
                var base64data = reader.result.split(",")[1];

                while (base64data.length % 4 !== 0) {
                    base64data += "=";
                }

                console.log(base64data);

                $.ajax({
                    url: "/classify",
                    type: "POST",
                    data: {
                        image: base64data,
                    },
                    contentType: "application/x-www-form-urlencoded",
                    success: function (data) {
                        console.log(data);
                    },
                    error: function (err) {
                        console.log(err);
                    },
                });

                // $.ajax({
                //     url: "/tmp",
                //     type: "POST",
                //     data: { image: reader.base64data },
                //     contentType: "application/x-www-form-urlencoded",
                //     success: function (data) {
                //         $("#img-prev")
                //             .attr(
                //                 "src",
                //                 "http://127.0.0.1:4000/static/temp/" +
                //                     data.image_path
                //                         .split("\\")
                //                         .pop()
                //                         .split("/")
                //                         .pop()
                //             )
                //             .attr(
                //                 "data-trigger",
                //                 "data:image/png;base64," + reader.base64data
                //             );
                //     },
                //     error: function (err) {
                //         console.log(err);
                //     },
                // });
            };

            reader.readAsDataURL(file); // jangan lupa hapus var baseImg, karena tidak perlu di assign lagi
        }
    });

    $("#btn-process").click(function (e) {
        e.preventDefault();

        $.ajax({
            url: "/classify",
            type: "POST",
            data: {
                image: reader.base64data,
            },
            contentType: "application/x-www-form-urlencoded",
            success: function (data) {
                console.log(data);
            },
            error: function (err) {
                console.log(err);
            },
        });
    });
});
