'use strict';

(function() {
	window.addEventListener('load', init);
	function init() {
		console.log('hello world');
		let preview = document.getElementById('preview_image');
	}
	function previewImage(image) {
		console.log(image);
    	window.open("{{url_for('static', filename=image)}}", "_blank");
	}
})();
