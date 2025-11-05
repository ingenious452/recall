# Recall

Have you ever have problem managing large number of project when you are not sure 
in which directory has the project you were working on 

> recall help you keep track of all your project directory from command line


## How to use

1. Open directory

```cmd
recall get <id> --name 
```

2. Save directory

```cmd
recall save <project_name> --path <project_path>
```
```--path``` defaults to the **current working directory**

3. Delete directory

```cmd
recall delete <project_name>
```

4. Update directory
```cmd
recall update <project_name> --path <updated_project_path>
```
```--path``` defaults to the **current working directory**

5. List directories
```cmd
recall show
```

