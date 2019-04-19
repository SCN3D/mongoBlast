//执行blast
const fs = require("fs");
const path = require("path");
const exec = require('child_process').exec;

async function ProcessBlast(cmdStr, filePath){
  return await helper(cmdStr, filePath);
}

function helper(cmdStr, filePath){
  let res = [];

  function cmd(){ 
    return new Promise((resolve, reject) => {
      exec(cmdStr, (error, stdout) => {
        console.log(stdout)
        if (error) {
          console.log(`exec error: ${error}`);
          reject();
        }    
        else {
          console.log(33)
          resolve(3);
        }
      })
    })
  }

  function read1(){ 
    return new Promise((resolve, reject) => {
      fs.readFile(filePath + 'blast_output.txt', 'utf-8', (err, data) => {
        if(err) {
          console.log(err);
          resolve('error')
        }
        else{
          res.push(data);
          resolve(res)
        }
      })    
    })
  }

  function read2(){ 
    return new Promise((resolve, reject) => {
      let finalData = "";
      let filesDir = fs.readdirSync(filePath);
      filesDir.forEach(file => {
        if(file !== 'blast_output.txt' && file !== 'sequence.fasta'){
          let finalPath = path.join(filePath, file);
          let data = fs.readFileSync(finalPath, 'utf-8');
          finalData += data;
        }
      })   
      res.push(finalData);
      resolve(res)
    })
  }
  
  //依次执行命令，包括blast的各种命令和读取结果，出现错误则返回fail
  return cmd().then(read1).then(read2).catch(err => {
    console.log('cmdfail')
    return 'fail';
  })
}

module.exports = ProcessBlast;
