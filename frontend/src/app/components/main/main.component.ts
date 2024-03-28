import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { Tab } from '../../models/tab';
import { MainService } from '../../services/main.service';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrl: './main.component.css'
})

export class MainComponent implements OnInit {

  @ViewChild('containerTabs') containerTabs!: ElementRef;
  @ViewChild('inputConsole') inputConsole!: ElementRef;
  @ViewChild('outputConsole') outputConsole!: ElementRef;

  //Titulo Reporte
  report_name: string = "";
  //Pestañas
  tabs: Tab[] = [];
  currentTab: number = 0;
  //Consola Input
  linesInputConsole: string[] = [];
  //Consola Output
  outputConsoleContent = '';
  linesOutputConsole: string[] = [];
  //[ruta, nombre, contenido_anterior, contenido_actual]
  //Symbols
  symbols: any[] = [];
  //Errores
  errors: any[] = [];


  constructor(private service: MainService) { }

  ngOnInit(): void {
    this.tabs.push(new Tab("", "sin_titulo", "", ""));
    this.updateLinesInputConsole();
    this.updateLinesOutputConsole();
  }

  // Option Open
  openFileExplorer(inputFile: HTMLInputElement) {
    inputFile.click();
  }

  openFile(event: any) {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      const filePath = event.target.value;
      const fileName = filePath.split('\\').pop() || filePath.split('/').pop();
      const fileReader = new FileReader();
      fileReader.onload = (e: any) => {
        const fileContent = e.target.result;
        this.tabs[this.currentTab].ruta = filePath;
        this.tabs[this.currentTab].nombre = fileName;
        this.tabs[this.currentTab].contenido_anterior = fileContent;
        this.tabs[this.currentTab].contenido_actual = fileContent;
        this.updatesLines_updateConsole();
      };
      fileReader.readAsText(selectedFile);
    }
  }

  // Option Save
  async save() {  
    await Swal.fire({
      title: 'Nombre Archivo',
      input: 'text',
      inputValue: this.tabs[this.currentTab].nombre + '.qc',
      inputAttributes: { spellcheck: 'false' },
      showCancelButton: true,
      confirmButtonText: 'Guardar',
      cancelButtonText: 'Cancelar',
      inputValidator: (value) => {
        if (!value) {
          return '¡Complete el campo vacio!';
        } else {
          return null;
        }
      },
    }).then((result) => {
      if (result.isConfirmed) {
        const nombreIngresado = result.value;
        this.tabs[this.currentTab].nombre = nombreIngresado;
        this.tabs[this.currentTab].contenido_anterior = this.tabs[this.currentTab].contenido_actual;
        Swal.fire('Archivo guardado exitosamente.', `Archivo guardado en C:\\Users\\Luis T\\Documents\\QueryCrypterApp\\${nombreIngresado}`, 'success');
      }
    });
  }

  // Option Run
  run() {
    var code = this.tabs[this.currentTab].contenido_actual
    const postData = { "code": code };
    
    this.service.postCode(postData).subscribe(
      (response) => {
        var r = response as any;
        this.errors = r.errors;
        this.symbols = r.symbols;
        if (r.errors.length == 0) {
          this.linesOutputConsole = r.console.split('\n');
          this.outputConsole.nativeElement.value = r.console;
          this.outputConsoleContent = r.console;
          this.outputConsole.nativeElement.style.height = 'auto';
          this.outputConsole.nativeElement.style.height = this.outputConsole.nativeElement.scrollHeight + 'px';
        } else {
          let e: string = "";
          for (let i = 0; i < r.errors.length; i++) {
            if (i == 0) {
              if (r.errors[i].type == "Lexico") {
                e += "Error lexico en "+r.errors[i].error+", linea "+r.errors[i].line+", columna "+r.errors[i].column+".";
              } else if (r.errors[i].type == "Sintactico") {
                e += "Error sintactico en "+r.errors[i].error+", linea "+r.errors[i].line+", columna "+r.errors[i].column+".";
              }
            } else {
              if (r.errors[i].type == "Lexico") {
                e += "\nError lexico en "+r.errors[i].error+", linea "+r.errors[i].line+", columna "+r.errors[i].column+".";
              } else if (r.errors[i].type == "Sintactico") {
                e += "\nError sintactico en "+r.errors[i].error+", linea "+r.errors[i].line+", columna "+r.errors[i].column+".";
              }
            }
          }
          this.linesOutputConsole = e.split('\n');
          this.outputConsole.nativeElement.value = e;
          this.outputConsoleContent = e;
          this.outputConsole.nativeElement.style.height = 'auto';
          this.outputConsole.nativeElement.style.height = this.outputConsole.nativeElement.scrollHeight + 'px';
        }

      },
      (error) => {
        console.error('Error:', error);
      }
    );
    
  }

  // Option Reports
  getErrorsReport() {
    this.report_name = "Reporte de Errores";
  }

  getSymbolsReport() {
    this.report_name = "Reporte de Simbolos";
  }

  // Tabs
  select_tab(i:number) {
    this.currentTab = i;
    this.updatesLines_updateConsole();
  }

  add_tab() {
    if (this.tabs.length < 4) {
      this.tabs.push(new Tab("", "sin_titulo", "", ""));
      this.currentTab = this.tabs.length - 1;
      this.updateLinesInputConsole();
    } else {
      Swal.fire('Oops...', 'Ha llegado al límite de pestañas.', 'error')
    }
  }
  
  async delete_tab(i:number) {
    var respuesta: Boolean = true;
    if (this.tabs[i].contenido_anterior != this.tabs[i].contenido_actual) {
      const { isConfirmed } = await Swal.fire({
        title: 'Advertencia',
        text: 'Los cambios no guardados se perderán. ¿Desea continuar?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Si',
        cancelButtonText: 'No',
      });
      if (!isConfirmed) {
        respuesta = false;
      }
    }
    if (respuesta) {
      if (this.tabs.length > 1) {
        if (this.currentTab == i) {
          if (i != 0) {
            this.currentTab = i-1;
          }
          this.tabs.splice(i, 1);
        } else {
          if (this.currentTab > i) {
            this.currentTab = this.currentTab-1;
          }
          this.tabs.splice(i, 1);
        }
      } else {
        this.tabs[i] = new Tab("", "sin_titulo", "", "");
      }
      this.updatesLines_updateConsole();
    }
  }

  // Consoles
  autoExpand(textarea: HTMLTextAreaElement) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
  }

  updateLinesInputConsole() {
    this.linesInputConsole = this.tabs[this.currentTab].contenido_actual.split('\n');
  }

  updateLinesOutputConsole() {
    this.linesOutputConsole = this.outputConsoleContent.split('\n');
  }

  updatesLines_updateConsole() {
    this.updateLinesInputConsole();
    this.inputConsole.nativeElement.value = this.tabs[this.currentTab].contenido_actual;
    this.inputConsole.nativeElement.style.height = 'auto';
    this.inputConsole.nativeElement.style.height = this.inputConsole.nativeElement.scrollHeight + 'px';
  }

  onKeyPress(event: KeyboardEvent) {
    const teclaPresionada = event.key;
    if (teclaPresionada === 'Tab') {
      event.preventDefault();
      //this.inputConsole.nativeElement.setSelectionRange(start+1, start+1);
      const i = this.inputConsole.nativeElement.selectionStart;
      const principio = this.tabs[this.currentTab].contenido_actual.slice(0, i);
      const final = this.tabs[this.currentTab].contenido_actual.slice(i);
      this.tabs[this.currentTab].contenido_actual = principio+"\t"+final;
    }
  }

}