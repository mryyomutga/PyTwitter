var exec = require('child_process').exec;
var ind = 10;
cmd = 'python Bot.py '
setInterval(function(){
	cmd += ind
	exec(cmd, function(error, stdout, stderr) {
	  // シェル上でコマンドを実行できなかった場合のエラー処理
	  if (error !== null) {
	    console.log('exec error: ' + error);
	    return;
	  }
	  ind += 1;
	  cmd = 'python PyTwitter.py '
	  // シェル上で実行したコマンドの標準出力が stdout に格納されている
	  console.log('stdout: ' + stdout);
	});
}, 1000 * 10)
