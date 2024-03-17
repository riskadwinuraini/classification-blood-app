$(document).ready(function () {
    // Fungsi upload image ketika dipilih
    $("#upload-img").change(function (event) {
        var files = event.target.files;

        if (files && files.length > 0) {
            var file = files[0];

            var reader = new FileReader();
            reader.onload = function (e) {
                var base64data = e.target.result;

                $.ajax({
                    url: "/submit",
                    type: "POST",
                    data: { image: base64data },
                    contentType: "application/x-www-form-urlencoded",
                    processData: false,
                    success: function (data) {
                        console.log(data);
                        // $("#result").html(data);
                    },
                    error: function (err) {
                        console.log(err);
                    },
                });
            };

            reader.readAsDataURL(file);
        }
    });
});
