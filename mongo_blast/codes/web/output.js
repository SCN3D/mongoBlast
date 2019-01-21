import React, { Component } from 'react';
import swal from 'sweetalert';
import $ from 'jquery';
import saveAs from 'file-saver';
import JSZip from 'jszip';
import Element from '../../children/element/element';
import style from './output.css';
import Slider from 'react-bootstrap-slider';
import Select from 'react-select';
import _ from 'underscore';
import './slider.css';


const options = [
  { label: 'Phosphotyrosine', value: "\"Phosphotyrosine\"" },
  { label: 'Phosphoserine', value: "\"Phosphoserine\"" },
  { label: 'Dimethylated arginine', value: "\"Dimethylated arginine\"" },
  { label: 'Symmetric dimethylarginine', value: "\"Symmetric dimethylarginine\"" },
  { label: 'Asymmetric dimethylarginine', value: "\"Asymmetric dimethylarginine\"" },
  { label: 'N-linked (GlcNAc) asparagine', value: "\"N-linked (GlcNAc) asparagine\"" },
  { label: 'S-palmitoyl cysteine', value: "\"S-palmitoyl cysteine\"" },
  { label: 'Phosphothreonine', value: "\"Phosphothreonine\"" },
  { label: 'Omega-N-methylarginine', value: "\"Omega-N-methylarginine\"" },
  { label: 'Pyrrolidone carboxylic acid', value: "\"Pyrrolidone carboxylic acid\"" },
  { label: 'N6-acetyllysine', value: "\"N6-acetyllysine\"" },
  { label: 'N6-methyllysine', value: "\"N6-methyllysine\"" },
  { label: 'N6,N6-dimethyllysine', value: "\"N6,N6-dimethyllysine\"" },
  { label: 'N6,N6,N6-trimethyllysine', value: "\"N6,N6,N6-trimethyllysine\"" },
  { label: 'Glycyl lysine isopeptide (Lys-Gly)(interchain with G-Cter in SUMO)', value: "\"Glycyl lysine isopeptide (Lys-Gly)(interchain with G-Cter in SUMO)\"" },
  { label: 'Glycyl lysine isopeptide (Lys-Gly)(interchain with G-Cter in ubiquitin)', value: "\"Glycyl lysine isopeptide (Lys-Gly)(interchain with G-Cter in ubiquitin)\"" }
];


class Output extends React.Component {

  constructor(props){
    super(props);
    this.state = {
      step: 1,
      min: 0,
      max: 100,
      curValue: 70,
      current: 1,
      currentSeq: '',
      blastOptions: [],
      blastRes: [],
      blasting: false,
      visible : false
    }
  }
/*  handleSelect = blastOptions => {
    this.setState({ blastOptions: blastOptions });
    console.log(`Option selected:`, blastOptions);
  }*/
  handle3D = () => {
    var fs = require( 'fs' );
    var out = '';
    let resi = "";
    let seq = this.state.currentSeq.split("\n")[1];
    let position = Object.keys(this.props.results[0]).join("%2C");
    let url = "https://g2s.genomenexus.org/api/alignments/residueMapping?sequence="+seq+"&positionList="+position;
    function parsePosition(value, index, array){
      resi = resi + value.pdbPosition + ", ";
    }
    var disurl = '';
    var selection = '';
    $.getJSON(url, function(data) {
      data[0].residueMapping.forEach(parsePosition);
      resi = resi.replace(/,\s*$/, "");
      let chain = data[0].chain;
      selection = resi+":"+chain;
      let pdb = data[0].pdbId;
      disurl = "rcsb://"+pdb;
      let obj = {
        url: disurl,
        selection: selection
      };
      out = "http://18.223.55.81:5000/display3d?url="+obj.url+"&sele="+obj.selection;
      window.open(out);
    });
   
  }
  handleDownload = () => {
    let zip = new JSZip();
    zip.file('input.fasta', this.props.originalInput);
    zip.file('output.txt', this.props.originalResults);
    zip.generateAsync({type: 'blob'}).then( content => {
      saveAs(content, 'sequence.zip');
    });
  }

  handleBlast = () => {
  	let currentSeq = this.state.currentSeq;
  	if(this.state.blasting === true){
      swal({
        text: "Please wait for blast processing!",
        icon: "info",
        button: "Got it!",
        timer: 3000
      });
      return;
  	}
/*    if(this.state.blastOptions.length == 0){
      swal({
        text: "Please select at least one ptm!",
        icon: "info",
        button: "Got it!",
        timer: 3000
      });
      return;
    }*/

    this.setState({
    	blasting: true
    })
    $.ajax(
      {
        type: 'post',
        url: '/blast',
        data: {
          'userId': localStorage.getItem("userId"),
          'seq': this.state.currentSeq,
          'blastOptions': this.props.model
        },
        success: data =>{
        	if(currentSeq !== this.state.currentSeq) return;
          if(data){

          	/* set blast result */
            let res = data[0].split('\n');
            res.shift();
            res = res.map(e => {
            	let title = e.substring(0, 14).replace(/\s/g, "");
            	let seq = e.substring(14).split('');
              return {
              	'title': title, 
              	'seq': seq,
              	'pos': []
              };
            })
            res = res.slice(0, 15);

            /* set position */
            let pos = data[1].split('\n');
            pos.map(e => {
            	e = e.split(' ');
            	let title = e[0];
            	if(e.length > 1){
            		e.splice(0, 1);
	            	for(let obj of res){
	            		if(obj['title'] == title){
	            			obj['pos'] = obj['pos'].concat(e);
	            		}
	            	}           		
            	}
            })
            this.setState({
            	blasting: false,
              blastRes: res
            })
          }
        },
        error: (XMLHttpRequest, textStatus, errorThrown) => {
        	if(currentSeq !== this.state.currentSeq) return;
        	this.setState({
        		blasting: false
        	})
          swal({
          	title: "error",
          	text: "Please try again later!",
          	icon: "info",
          	button: "Got it!",
          	timer: 3000
        	});
                  console.log(XMLHttpRequest.status);
                  console.log(XMLHttpRequest.readyState);
                  console.log(textStatus);
            }
      }
    )    
  }

  changeValue = () => {
    this.setState({
      curValue: this.sliderRef.getValue()
    });
  };

  pageBack = () => {
    if(this.state.current === 1) return;
    this.setState({
      current: this.state.current - 1
    })
  }

  pageForward = () => {
    if(this.state.current === this.props.input.length) return;
    this.setState({
      current: this.state.current + 1
    })
  }

  changePage = e => {
    let pageNumber = Number(e.target.value);
    if(pageNumber > 1 && pageNumber <= this.props.input.length){
      this.setState({
        current: pageNumber
      });      
    }

  };

  shouldComponentUpdate(nextProps, nextState) {
    if(this.props.showOutput === false && nextProps.showOutput === false){
      console.log("no");
      return false;
    }
    if(_.isEqual(this.props, nextProps) && _.isEqual(this.state, nextState)){
      console.log(nextProps)
      console.log(this.props)
      console.log("no");
      return false;
    }
    //reset page number to 1 when start a new job
    if(nextProps.title.length <= 0){
    	if(this.state.currentSeq !== ''){
    		this.setState({
    			currentSeq: ''
    		})
    	}
    	if(this.state.blasting !== false){
    		this.setState({
    			blasting: false
    		})
    	}
      this.setState({
        current: 1,
      })
    }
    console.log("yes");
    return true;
  }

  componentDidUpdate(){
    let current = this.state.current - 1;
    let title = this.props.title || [];
    let seq = this.props.input || [];
    title = title[current] || '';
    seq = seq[current] || [];
    seq = seq.join('');
    seq = title + '\n' + seq;
    if(this.state.currentSeq !== seq){
      this.setState({
        currentSeq: seq
      })
    }
    if(this.props.title.length === 0){
      this.setState({
        blastRes: []
      })
    }
  }

  render(){
    let input = this.props.input;
    let index = this.state.current - 1;
    let e = input[index] ||[]; //In case of the input hasn't been received
    let items;
/*    let { blastOptions } = this.state.blastOptions;*/
    let blastRes = this.state.blastRes;

    //Received output
    if(this.props.title.length > 0){
      items = (
          <div key = {index} className = {style.item}>
            <button className = {style.title}>{this.props.title[index]}</button>
            <div className = {style.seqs}>
              <div className = {style.seq}>
                <label></label>
                {e.map((e1, index1) => {
                  return <Element type = 'pos' value = {index1 + 1} key = {'pos' + index1}/>
                })}
              </div>
              <div className = {style.seq}>
                <label>Sequence</label>
                {e.map((e2, index2) =>{
                  return <Element type = 'seq' value = {e2} id = {index2 + 1} curValue = {this.state.curValue} results = {this.props.results[index]} key = {'seq' + index2}/>
                })}
              </div>
              <div className = {this.state.blasting ? style.hide: style.blast}>
                {blastRes.map((e3, index3) => {
                  return (
                    <div className = {style.seq} key = {e3['title']}>
                      <label>{e3['title']}</label>
                      {e3['seq'].map((e4, index4) => {
                        return <Element type = 'blast' value = {e4} index = {index4 + 1} pos = {e3['pos']} key = {e3['title'] + index4}/>
                      })}
                    </div>
                  )
                })}
              </div>
			        <div className = {this.state.blasting ? style.blastLoading: style.hide}>
			          <div className = {style.loader}>
			            <div className = {style.dot}></div>
			            <div className = {style.dot}></div>
			            <div className = {style.dot}></div>       
			            <div className = {style.dot}></div>
			            <div className = {style.dot}></div>                   
			          </div>
			        </div>
            </div>
            <div className = {style.options}>
              <h3>Advanced Options</h3>
              <div className = {style.option}>
                <button onClick = {this.handleBlast}>Blast</button>
                <Select className = {style.select} options={options} isMulti closeMenuOnSelect={false} onChange = {this.handleSelect} />
              </div>
              <div className = {style.option}>
                <button className = {style.download} onClick = {this.handleDownload}>Download</button>
              </div>
              <div className = {style.option}>
                <button className = {style.download} onClick = {this.handle3D}>3D</button>
              </div>
            </div>           
          </div>
      )
    }

    //Haven't received output yet
    else if(!this.state.blasting){
      items = (
        <div className = {style.loading}>
          <div className = {style.loader}>
            <div className = {style.dot}></div>
            <div className = {style.dot}></div>
            <div className = {style.dot}></div>       
            <div className = {style.dot}></div>
            <div className = {style.dot}></div>                   
          </div>
        </div>
      )
    }

    return (

          <div className = {style.output}>
            <div className = {style.holder}>
              <div className = {style.slider}>
                <span style={{ marginRight: "15px" }}>{this.state.min}</span>
                <Slider
                  id="input-slider"
                  ref={e => {
                    if (e) this.sliderRef = e.mySlider;
                  }}
                  value={this.state.curValue}
                  slideStop={this.changeValue}
                  step={this.state.step}
                  min={this.state.min}
                  max={this.state.max}
                />
                <span style={{ marginLeft: "15px" }}>{this.state.max}</span>
              </div>
              <div className = {style.items}>
                {items}
              </div>
              <div className = {style.page}>
                <span onClick = {this.pageBack}>&lt;</span>
                <span><input type = "number" value = {this.state.current > 0 ? this.state.current : ""} min = "1" max = {this.props.input.length} onChange = {this.changePage}/> &nbsp; of &nbsp; {this.props.input.length}</span>
                <span onClick = {this.pageForward}>&gt;</span>
              </div>
            </div>
          </div>

    );
  }
}


export default Output