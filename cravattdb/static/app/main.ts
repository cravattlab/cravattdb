import { bootstrap } from '@angular/platform-browser-dynamic';
import { ROUTER_PROVIDERS } from '@angular/router';
import {enableProdMode} from '@angular/core';
enableProdMode();

import { AppComponent } from './app.component';

bootstrap(AppComponent, [ROUTER_PROVIDERS]);