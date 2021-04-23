<?php
	$success = 0;
	$uploadFile = '';
	$path = 'upload/';
	$file = $path . basename( $_FILES['file']['name']);
	if(@move_uploaded_file($_FILES['file']["tmp_name"], $file)){
		$success = 1;
		$uploadFile = $file;
	}
?>
<script type="text/javascript">window.alert(<?php echo $success; ?>);</script>
