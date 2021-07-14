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
            <div style="display: flex; align-item: center; margin-bottom: 20px;">
                <div class="icon" style="flex: 0 0 auto;">
                    <i class="far ${obj.icon} fa-lg" style="color: ${obj.color}"></i>
                </div>
                <div class="px-3 " style="flex: 1 1 auto;">
                <h4>${obj.title}</h4>
                ${obj.description}
                </div>
            </div>
            <button id="btn-back" type="button" class="btn btn-primary w-100">Try Another</button>
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
    
        console.log(article);

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
                    description: "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Vitae iure impedit quibusdam? Officiis tempora commodi odit fuga, aliquam harum aliquid velit sapiente aspernatur saepe magni laboriosam, consequuntur dolor animi dolorum."
                };
            } else {
                result = {
                    icon: "fa-smile",
                    color: "green",
                    title: "LIGITIMATE",
                    description: "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Vitae iure impedit quibusdam? Officiis tempora commodi odit fuga, aliquam harum aliquid velit sapiente aspernatur saepe magni laboriosam, consequuntur dolor animi dolorum."
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
