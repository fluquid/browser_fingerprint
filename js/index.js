/**
scripts to create fingerprints on browser client and send results to
    flask web service for further processing.
*/

function analyzeNavigator() {
    res = {};

    // TODO: plugins, mimetypes
    for (var name in window.navigator) {
        res[name] = window.navigator[name];
    }
    console.log('navigator', res);
    return res;
}


function getGlobalVars() {
    res = [];
    Object.getOwnPropertyNames(window).sort().forEach(function(val) {
        res.push(val);
    });
    console.log('globalVars', res);
    return res;
}


function getBeaverBird() {
    var res = BeaverBird.data();
    console.log('beaverbird', res);
    return res;
}


function getClientJs() {
    var client = new ClientJS();
    res = {}
    Object.getOwnPropertyNames(ClientJS.prototype).forEach(function (val) {
        if (typeof ClientJS.prototype[val] === 'function') {
            var name = val.replace(/^get|is/, '');
            res[name] = client[val]();
        }
    });
    console.log('clientjs', res);
    return res;
}


function analyzeEnv() {
	var deferred = $.Deferred()
	new Fingerprint2().get(function(result, components){
		res = {}

        components.forEach(function (val) {
            res[val.key] = val.value;
        });
        console.log('fingerprintjs2', res)
        deferred.resolve(res);
	})
	return deferred.promise()
	.then(function (components) {
        var navigator = analyzeNavigator();
        var globalVars = getGlobalVars();
        return {
            'fingerprintjs2': components,
            'clientjs': getClientJs(),
            'beaverbird': getBeaverBird(),
            'navigator': analyzeNavigator(),
            //'globalVars': getGlobalVars()
        };

    });
}


function postResults(data, success) {
    var url = '/postResults';
    var json_data = JSON.stringify(data)
    return $.post(url, json_data, success);

}


function fp_main(browser, headers) {
	analyzeEnv()
	.then(function(results) {
		results['browser'] = browser;
        results['headers'] = headers;
		postResults(results, function(data) {
			//document.write('<div id="fingerprint"></div>');
			document.write(data);
		});
	});
};
