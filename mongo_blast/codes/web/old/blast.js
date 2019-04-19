//这个文件是blast请求的入口文件，根据用户的输入生成各种参数，然后调用中间件processBlast来执行，并返回结果
const fs = require( 'fs' );
const path = require('path');
const processBlast = require("../middlewares/processBlast");
const exec = require('child_process').exec;
const rimraf = require("rimraf");


function mkDirByPathSync(targetDir, { isRelativeToScript = false } = {}) {
  const sep = path.sep;
  const initDir = path.isAbsolute(targetDir) ? sep : '';
  const baseDir = isRelativeToScript ? __dirname : '.';

  return targetDir.split(sep).reduce((parentDir, childDir) => {
    const curDir = path.resolve(baseDir, parentDir, childDir);
    try {
      fs.mkdirSync(curDir);
    } catch (err) {
      if (err.code === 'EEXIST') { 
        return curDir;
      }

      // To avoid `EISDIR` error on Mac and `EACCES`-->`ENOENT` and `EPERM` on Windows.
      if (err.code === 'ENOENT') { // Throw the original parentDir error on curDir `ENOENT` failure.
        throw new Error(`EACCES: permission denied, mkdir '${parentDir}'`);
      }

      const caughtErr = ['EACCES', 'EPERM', 'EISDIR'].indexOf(err.code) > -1;
      if (!caughtErr || caughtErr && curDir === path.resolve(targetDir)) {
        throw err; // Throw if it's just the last created dir.
      }
    }

    return curDir;
  }, initDir);
}

let fn_blast = async(ctx, next) => {

  let userId = ctx.request.body.userId;
  let seq = ctx.request.body.seq;
  let blastOptions = ctx.request.body.blastOptions;
  let options = "";
  for(let e of blastOptions){
  	options = options + e['value'] + " ";
  }
  let inputFile = 'sequence.fasta';

  //File path for system command
  let inputFileUrl = `~/musite/users/upload-files/${userId}/blast/${inputFile}`;
  let backgroundSeqsUrl = '~/mongoBlast/mongo_blast/background_seqs.fasta';
  let formatUrl = '~/mongoBlast/mongo_blast/format2.txt';
  let blastParseUrl = '~/mongoBlast/mongo_blast/blast_parse.py';
  let blastUrl = `~/musite/users/upload-files/${userId}/blast/`;

  //File path for node.js
  let blast_root = `~/musite/users/upload-files/${userId}`;
  let blastPath = `~/musite/users/upload-files/${userId}/blast/`;
  let inputFilePath = `~/musite/users/upload-files/${userId}/blast/${inputFile}`;

  mkdir(blastPath, inputFilePath, seq);

  let cmdStr1 = `cd $HOME/mongoBlast/mongo_blast && makeblastdb -in background_seqs.fasta -dbtype prot`;
  let cmdStr2 = `cd $HOME/mongoBlast/mongo_blast && blastp -task blastp -query ${inputFileUrl} -db background_seqs.fasta -evalue 1e-5 -num_descriptions 100 -num_alignments 100 -outfmt 2 -out ${formatUrl}`;
  let cmdStr3 = `cd $HOME/mongoBlast/mongo_blast && python ${blastParseUrl} -l ${formatUrl} -ptms ${options} -o ${blastUrl}`;

  let new_cmd = `cd $HOME/mongoBlast/mongo_blast && python user_query.py -ptms ${options} -o ${blastUrl}`;

  let result = await processBlast(new_cmd, blastPath);
  ctx.response.body = await result;
}

//在用户目录下生成blast目录
function mkdir(blastPath, inputFilePath, seq){
  if(fs.existsSync(blastPath)){
    rimraf(blastPath, err => {
      if(err){
        console.log(err);
      }
      else{
        mkDirByPathSync(blastPath);  
        fs.writeFileSync(inputFilePath, seq);      
      }
    })    
  }
  else {
    mkDirByPathSync(blastPath);
    fs.writeFileSync(inputFilePath, seq);
  }
  
}

module.exports = {
	'POST /blast': fn_blast
};

//cd $HOME/mongoBlast/mongo_blast && blastp -task blastp -query $HOME/musite/users/upload-files/jyuchi@mail.missouri.eduuuu/blast/sequence.fasta -db background_seqs.fasta -evalue 1e-5 -num_descriptions 100 -num_alignments 100 -outfmt 2 -out $HOME/mongoBlast/mongo_blast/format2.txt
//cd $HOME/mongoBlast/mongo_blast && python $HOME/mongoBlast/mongo_blast/blast_parse.py -l $HOME/mongoBlast/mongo_blast/format2.txt -ptms Phosphotyrosine -o $HOME/musite/users/upload-files/jyuchi@mail.missouri.eduuuu/blast/

//cd $HOME/mongoBlast/mongo_blast && blastp -task blastp -query example.fasta -db background_seqs.fasta -evalue 1e-5 -num_descriptions 20 -num_alignments 20 -outfmt 2 -out format2.txt
//cd $HOME/mongoBlast/mongo_blast && python blast_parse.py -l format2.txt -ptms Phosphotyrosine -o other   