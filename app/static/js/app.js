// Template for Analyzer Form
const tmplAnalyzerForm = () => {
    return `
        <div>
            <div class="form-group pb-3">
                <label for="article-title" class="form-label">Title</label>
                <input type="text" name="article-title" class="form-control" id="article-title" placeholder="Article Title">
            </div>
            <div class="form-group pb-3">
                <label for="article-body" class="form-label">Article Body</label>
                <textarea id="article-body" class="form-control" rows="5"></textarea>
            </div>
            <button id="btn-analyze" type="button" class="btn btn-primary w-100">Analyze</button>
        </div>
    `;
};

// Template for Analyzer Results
const tmplAnalyzerResults = (obj) => {
    return `
        <div class="results">
            <div class="my-4" style="display: flex; align-items: center;">
                <div class="icon" style="flex: 0 0 auto;">
                    <i class="far ${obj.icon} fa-lg" style="color: ${obj.color}"></i>
                </div>
                <div class="px-3 " style="flex: 1 1 auto;">
                <h4>${obj.title}</h4>
                ${obj.description}
                </div>
            </div>
            <button id="btn-back" type="button" class="btn btn-primary w-100 mt-3">Try Another</button>
        </div>
    `;
};

// Document Ready
$(document).ready(function() {
    // Event Listeners
    // Analyze Button Click Event
    $("body").on("click", "button#btn-analyze", function(event) {
        event.preventDefault();
        let article = {
            title: $("#article-title").val().trim(),
            body: $("#article-body").val().trim()
        }

        // API call to ML Article Analyzer
        $.ajax({
            url: "/api/v1.0/analyze",
            method: "POST",
            data: JSON.stringify(article),
            dataType: "json"
        }).then(function(data) {
            console.log(data);
            let result = {};

            if (data.prediction === "FAKE") {
                result = {
                    icon: "fa-angry",
                    color: "red",
                    title: "QUESTIONABLE",
                    description: "Not too sure about this news article. It looks a bit sketchy and probably shouldn't be trusted. Consider digging a little deeper, have a look around and try to find a more reliable source."
                };
            } else {
                result = {
                    icon: "fa-smile",
                    color: "green",
                    title: "LIGITIMATE",
                    description: "The news article looks ligitimate. As with anything on the Internet you should check the sources to be on the safe side, but so far we like what we're reading."
                };
            }

            $("div.content-container").empty();
            $("div.content-container").html(tmplAnalyzerResults(result));
        });
    
    });
    
    // Retry Button Click Event
    $("body").on("click", "button#btn-back", function(event) {
        event.preventDefault();
        $("div.content-container").empty();
        $("div.content-container").html(tmplAnalyzerForm);
    });
});
