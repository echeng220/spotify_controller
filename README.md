## Back-End (Django)
To run Django, both Apache and mod_wsgi must be installed.
### Apache Installation (Windows)
https://www.youtube.com/watch?v=oJnCEqeAsUk

Apache is required to run Django. To install Apache:

- Go to [Apache Lounge](https://www.apachelounge.com/download/)
- Download latest Apache binaries for Win64 (.zip file)
- Unzip to C: Drive (It must be unzipped to the C: Drive)
- In Command Prompt, navigate to the **bin** folder in the Apache24 folder
```cmd cd C:\Apache24\bin```
- Then run the following command:
```cmd httpd -k install```
- From the Start menu, open the Services window, and Start the Apache2.4 service
- In a browser tab, go to 127.0.0.1
- You should see "It works!" in the browser, which signals that the Apache installation was successful

### mod_wsgi Installation
mod_wsgi can be installed with pip:
```cmd pip install mod-wsgi```

### Django Installation
Django can be installed with pip:
```cmd pip install Django```
Django REST framework can be installed with pip:
```cmd pip install djangorestframework```

## Front-End (React)
Prerequisites: install npm and Node.js

Create or set up npm package (create package.json, node_modules directory etc.):
```cmd npm init -y```

Install webpack (transpiles source JS code into a single .js file):
```cmd npm i webpack webpack-cli --save-dev```

Install Babel (transpile into code that is browser friendly for all browsers):
```cmd npm i @babel/core babel-loader @babel/preset-env @bable/preset-react --save-dev```

Install React:
```cmd npm i react react-dom --save-dev```

Install pre-built components:
```cmd npm install @material-ui/core```
```cmd npm install @mui/material @emotion/react @emotion/styled```

So we can use async / await in .js code:
```cmd npm install @babel/plugin-proposal-class-properties```

Re-route pages from React app:
```cmd npm install react-router-dom```

Get icons from material-ui:
```cmd npm install @material-ui/icons```
```cmd npm install @mui/icons-material```

Note: To resolve npm dependency errors (see [post](https://stackoverflow.com/questions/72596908/could-not-resolve-dependency-error-peer-react16-8-0-17-0-0-from-materia)):
```cmd npm config set legacy-eer-deps true```
```cmd npm i```

Once npm packages are installed, create config files in the frontend folder:
1. babel.config.json
2. webpack.config.js

Then, modify the package.json to include scripts that tell webpack what to do when certain npm commands are run:
1. dev: run webpack in development mode, with watch (watches for changes in .js files, and recompiles output .js so browser can refresh with changes)
2. build: no watch

Django BE renders template, then passes template to React to manage.

To run development script:
```npm run dev```
where "dev" was defined in the package.json file.