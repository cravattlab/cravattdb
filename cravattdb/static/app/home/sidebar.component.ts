import { Component, ViewChild, AfterViewInit, ElementRef } from '@angular/core';

declare var $: any;

@Component({
    selector: 'sidebar',
    templateUrl: 'sidebar.html',
    styles: [`
        .sidebar {
            overflow-x: hidden;
        }
        .pusher {
            position: absolute!important;
            top: 0;
        }
    `]
})

export class SidebarComponent implements AfterViewInit {
    @ViewChild('sidebar') sidebarEl: ElementRef;
    options: {};
    sidebar: any;

    ngAfterViewInit() {
        let el = this.sidebarEl.nativeElement;

        const options = {
            transition:'overlay',
            dimPage: false,
            context: el.parentNode
        }

        this.sidebar = (command) => {
            $(el).sidebar(options).sidebar(command)
        };
    }
    
    show() {
        this.sidebar('show');
    }
    
    hide() {
        this.sidebar('hide');
    }
    
    toggle() {
        this.sidebar('toggle');
    }
}