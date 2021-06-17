<script src="bower_components/jquery/dist/jquery.min.js"></script>
        <script src="bower_components/bootstrap/dist/js/bootstrap.js"></script>
        <script src="js/ui-load.js"></script>
        <script src="js/ui-jp.config.js"></script>
        <script src="js/ui-jp.js"></script>
        <script src="js/ui-nav.js"></script>
        <script src="js/ui-toggle.js"></script>

        <script>
        	$('#rerunModal').on('show.bs.modal', function (event) {
			  var button = $(event.relatedTarget) // Button that triggered the modal
			  var company = button.data('company') // Extract info from data-* attributes
			  var campaign = button.data('campaign') // Extract info from data-* attributes
			  var brand = button.data('brand') // Extract info from data-* attributes
			  var assign = button.data('assign') // Extract info from data-* attributes
			  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
			  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
			  var modal = $(this)
			  // modal.find('.modal-title').text('Re Run Campaign "' + campaign + '"')
			  modal.find('.modal-body #company').val(company)
			  modal.find('.modal-body #campaign').val(campaign)
			  modal.find('.modal-body #brand').val(brand)
			  modal.find('.modal-body #preassign').val(assign)
			})
        </script>
</body>

</html>