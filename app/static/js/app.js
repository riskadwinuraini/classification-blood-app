$(document).ready(function () {
    var $modal = $("#modal");
    var image = document.getElementById("sample_image");
    var cropper;

    $("#upload-img").on("change", function () {
        var files = event.target.files;
        console.log(files);

        var done = function (url) {
            image.src = url;
            $modal.modal("show");
        };

        if (files && files.length > 0) {
            reader = new FileReader();
            reader.onload = function (event) {
                done(reader.result);
            };
            reader.readAsDataURL(files[0]);
        }
    });

    $modal
        .on("shown.bs.modal", function () {
            var finalCropWidth = 10;
            var finalCropHeight = 10;
            var finalAspectRatio = finalCropWidth / finalCropHeight;

            cropper = new Cropper(image, {
                aspectRatio: finalAspectRatio,
                viewMode: 3,
                cropBoxResizable: true,
                preview: ".preview",
                dragMode: "move"
            });
        })
        .on("hidden.bs.modal", function () {
            cropper.destroy();
            cropper = null;
        });

    $("#crop").click(function () {
        canvas = cropper.getCroppedCanvas({
            width: 220,
            height: 220,
            cropBoxResizable: false,
        });

        $modal.modal("hide");

        canvas.toBlob(function (blob) {
            var reader = new FileReader();

            reader.onload = function (event) {
                var base64data = reader.result.split(",")[1];

                while (base64data.length % 4 !== 0) {
                    base64data += "=";
                }

                $.ajax({
                    url: "/classify",
                    type: "POST",
                    data: {
                        image: base64data,
                    },
                    contentType: "application/x-www-form-urlencoded",
                    beforeSend: function () {
                        $("#progressModal").modal("show");
                    },
                    success: function (data) {
                        updateImagePreview(data);
                        createPieChart(data);
                        $(".main-label").text(data.label);
                        $(".main-probabilitas").text(
                            data.probabilities.main + "%"
                        );
                        $("#progressModal").modal("hide");
                        $("#upload-img").prop("disabled", true);
                    },
                    error: function (err) {
                        console.log(err);
                        $("#progressModal").modal("hide");
                    },
                });
            };

            reader.readAsDataURL(blob);
        });
    });
});

function updateImagePreview(data) {
    var imagePath = data.image_path
        ? "http://127.0.0.1:4000/static/temp/" +
          data.image_path.split("\\").pop().split("/").pop()
        : "";
    $("#img-prev").attr("src", imagePath);
}

function createPieChart(data) {
    var labels = Object.keys(data.probabilities.others);
    labels.unshift(data.label); // add the main label at the beginning

    var dataset = Object.values(data.probabilities.others);
    dataset.unshift(data.probabilities.main); // add the main probability at the beginning

    var ctx = document.getElementById("pieChart").getContext("2d");
    var myChart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "# of Votes",
                    data: dataset,
                    backgroundColor: [
                        "rgba(255, 99, 132, 0.2)",
                        "rgba(54, 162, 235, 0.2)",
                        "rgba(255, 206, 86, 0.2)",
                        "rgba(75, 192, 192, 0.2)",
                        "rgba(153, 102, 255, 0.2)",
                    ],
                    borderColor: [
                        "rgba(255, 99, 132, 1)",
                        "rgba(54, 162, 235, 1)",
                        "rgba(255, 206, 86, 1)",
                        "rgba(75, 192, 192, 1)",
                        "rgba(153, 102, 255, 1)",
                    ],
                    borderWidth: 1,
                },
            ],
        },
        options: {
            responsive: false,
        },
    });
}
