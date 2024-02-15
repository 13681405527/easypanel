#include <stdio.h>
#include <dirent.h> 
#include <sys/stat.h> 
#include <string.h> 

void file_list(const char *path) {
    DIR *dir;
    struct dirent *file_read;

    if ((dir = opendir(path)) == NULL) {
        perror("无法打开此目录");
        return;
    }

    while ((file_read = readdir(dir)) != NULL) {
        char file_path[PATH_MAX];


        snprintf(file_path, PATH_MAX, "%s/%s", path, file_read->d_name);


        if (strcmp(file_read->d_name, ".") == 0 || strcmp(file_read->d_name, "..") == 0)
            continue;

        struct stat info;
        if (stat(file_path, &info) == -1) {
            perror("无法获取文件");
            continue;
        }

        if (S_ISDIR(info.st_mode)) {
            printf("%s/\n", file_read->d_name);
            file_list(file_path);
        } else if (S_ISREG(info.st_mode)) {
    
            printf("%s\n", file_read->d_name);
        }
    }

    closedir(dir);
}

int main() {
    const char *directory_to_list = ".";
    file_list(directory_to_list);
    return 0;
}