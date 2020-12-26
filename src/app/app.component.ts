import { Component, Input, NgZone, OnInit, ViewChild} from '@angular/core';
import { CodeModel } from '@ngstack/code-editor/lib/models/code.model';
import { CanvasWhiteboardComponent, CanvasWhiteboardOptions, CanvasWhiteboardService, CanvasWhiteboardUpdate } from 'ng2-canvas-whiteboard';
import { BehaviorSubject, Observable } from 'rxjs';
import { debounceTime } from 'rxjs/operators';
import { CodeEditorService } from '@ngstack/code-editor';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit{
  @ViewChild('canvasWhiteboard') canvasWhiteboard: CanvasWhiteboardComponent;

  title = 'CanvasToCode';

  theme = 'vs-dark';

  draw$ = new BehaviorSubject<String>(null);

  codeModel: CodeModel = {
    language: 'python',
    uri: 'main.python',
    value: 'abc',
  };

  options = {
    contextmenu: true,
    fontSize: "16",
    smoothScrolling: true,
    cursorSmoothCaretAnimation: true,
    padding: {
      top: "10"
    },
    minimap: {
      enabled: true,
    },
  };

  canvasOn$ = new BehaviorSubject<boolean>(false);


  mouseup$: any;
  mousedown$: Observable<any>;
  mousemove$: any;
  mousehold$: any;
  x: number;
  y: number;
  _sub: any;

  mouseX = 0;
  mouseY = 0;
  colour = 'hotpink';
  canvas: any;
  mousedown = false;
  context: any;


  canvasOptions: CanvasWhiteboardOptions = {
    startingColor:"#4D000000",
    drawingEnabled: true,
    drawButtonEnabled: false,
    clearButtonEnabled: true,
    clearButtonClass: "clearButtonClass",
    clearButtonText: "Clear",
    undoButtonEnabled: false,
    redoButtonEnabled: false,
    colorPickerEnabled: false,
    shapeSelectorEnabled: false,
    fillColorPickerText: "Fill",
    strokeColorPickerText: "Stroke",
    saveDataButtonEnabled: false,
    saveDataButtonText: "Save",
    lineWidth: 3,
    strokeColor: "rgb(190,220,250)",
    shouldDownloadDrawing: true
  };

  constructor(private _canvasWhiteboardService: CanvasWhiteboardService,
              private _codeEditorService: CodeEditorService,
              private zone: NgZone) { }

  ngOnInit() {

    this.draw$.pipe(debounceTime(500))
              .subscribe(res => {
                  if(res) {
                    // let generatedString = this.canvasWhiteboard.generateCanvasDataUrl("image/jpeg", 1);
                    // this.canvasWhiteboard.downloadCanvasImage("image/png", generatedString, "0");
                    this.canvasWhiteboard.generateCanvasBlob((blob: any) => {
                      console.log(blob);
                      this.zone.run(() => {
                        this.codeModel =  {
                          language: 'python',
                          uri: 'main.python',
                          value: this.codeModel.value + `\n`,
                        };
                      });
                      
                   }, "image/png");
                    this._canvasWhiteboardService.clearCanvas();
                  }
              })
    

  }

  onDone_Drawing() {
    
    this.draw$.next("done");
    
  }

  canvasToggle() {
    this.canvasOn$.next(!this.canvasOn$.value);
  }
  
  // onCodeChanged(value) {
  //   console.log('CODE', value);
  // }

  onCanvasClear() {
    let update = new Array<CanvasWhiteboardUpdate>();
    this._canvasWhiteboardService.drawCanvas(update)
  }
}
