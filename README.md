# vue-project

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

## Floder api and Database

We use XAMPP as a server emulator. You can place the "api" folder in the directory path "xampp/htdocs/" after installing XAMPP.

## Floder Python

The file "omr_process_100.py" serves as the main code for checking exams with 1-100 questions according to the specified template.

## The necessary path needs to be changed according to the file location on your own Device.

### Stored python files

- "CheckAnswerView.vue" line 81 and 109 in "MultipleChoice-Checking-OMR-WebApp/src/views/CheckAnswerView.vue" for path where the "omr_process_100.py" file is stored.

### Xampp

- omr_process_100.py line 17 and 144
- "showImgStd.php" line 14 in "api/runPythonScript.php"
- "runPythonScript.php" line 15 in "api/runPythonScript.php"
