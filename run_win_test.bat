echo start surepatch.py...

echo 1. create config
c:\Python36\python.exe surepatch.py --action=save_config --team=dima --user=ws.bespalov@gmail.com --password=Test123!
timeout 3

echo 2. create platform autotest1
c:\Python36\python.exe surepatch.py --action=create_platform --platform=autotest1 --description="New Platform for Autotest"
timeout 3
echo 3. create project autotest_os_none - OS packages, collected by shell command
c:\Python36\python.exe surepatch.py --action=create_project --platform=autotest1 --project=autotest_os_none --target=os --method=auto --format=system
timeout 3
echo 4. create project autotest_os_path - OS packages, collected from shell command, unloaded to file
c:\Python36\python.exe surepatch.py --action=create_project --platform=autotest1 --project=autotest_os_path --target=os --method=auto --format=system --file=c:\windows_packages.txt
timeout 3
echo 5. create project autotest_pip_none - PIP Packages, collected from shell command
c:\Python36\python.exe surepatch.py --action=create_project --platform=autotest1 --project=autotest_pip_none --target=pip --method=auto --format=system
timeout 3
echo 6. create project autotest_pip_path - PIP packages, collected from shell command, unloaded to file
c:\Python36\python.exe surepatch.py --action=create_project --platform=autotest1 --project=autotest_pip_path --target=pip --method=auto --format=system --file=c:\pip_freeze_packages.txt
timeout 3
echo 7. create project autotest_req_path - Python packages from requirements.txt
c:\Python36\python.exe surepatch.py --action=create_project --platform=autotest1 --project=autotest_req_path --target=req --method=auto --format=system --file=c:\requirements.txt
timeout 3
echo 8. create project autotest_npm_none - NPM packages, collected from shell command (npm list --json) from root dir
c:\Python36\python.exe surepatch.py --action=create_project --platform=autotest1 --project=autotest_npm_none --target=npm --method=auto --format=system
timeout 3
echo 9. create project autotest_npm_path - NPM packages, collected from shell command (npm list --json) from root dir, unloaded to file
c:\Python36\python.exe surepatch.py --action=create_project --platform=autotest1 --project=autotest_npm_path --target=npm --method=auto --format=system --file=c:\npm.txt
timeout 3
echo 10. create project autotest_local_none - NPM packages, collected from shell command (npm list --json) from local dir
c:\Python36\python.exe surepatch.py --action=create_project --platform=autotest1 --project=autotest_local_none --target=npm_local --method=auto --format=system --file=c:\workspace\node
timeout 3
echo 11. create project autotest_npm_package_lock_path - NPM packages, collected from package-lock.json file
c:\Python36\python.exe surepatch.py --action=create_project --platform=autotest1 --project=autotest_npm_package_lock_path --target=package_lock_json --method=auto --format=system --file=c:\package-lock.json
timeout 3
echo 12. create project autotest_npm_package_json - NPM packages, collected from package.json file
c:\Python36\python.exe surepatch.py --action=create_project --platform=autotest1 --project=autotest_npm_package_json --target=package_json --method=auto --format=system --file=c:\package.json
timeout 3
echo 13. create project autotest_gem_none - Ruby packages, collected from shell command
c:\Python36\python.exe surepatch.py --action=create_project --platform=autotest1 --project=autotest_gem_none --target=gem --method=auto --format=system
timeout 3
echo 14. create project autotest_gem_path - Ruby packages, collected from shell commend, unloaded to file
c:\Python36\python.exe surepatch.py --action=create_project --platform=autotest1 --project=autotest_gem_path --target=gem --method=auto --format=system --file=c:\gem.list
timeout 3
echo 15. create project autotest_gemfile_path - Ruby packages, collected from Gemfile
c:\Python36\python.exe surepatch.py --action=create_project --platform=autotest1 --project=autotest_gemfile_path --target=gemfile --method=auto --format=system --file=c:\Gemfile
timeout 3
echo 16. create project autotest_gemfile_path - Ruby packages, collected from Gemfile.lock
c:\Python36\python.exe surepatch.py --action=create_project --platform=autotest1 --project=autotest_gemfile_lock_path --target=gemfile_lock --method=auto --format=system --file=c:\Gemfile.lock
timeout 3
echo 17. create project autotest_any_user_path - User packages formatted as name=version
c:\Python36\python.exe surepatch.py --action=create_project --platform=autotest1 --project=autotest_any_user_path  --method=auto --format=user --file=c:\user_packages.txt
timeout 3
echo 18. create project autotest_any_user_none - User packages asked from console
c:\Python36\python.exe surepatch.py --action=create_project --platform=autotest1 --project=autotest_any_user_none --method=manual --format=user
timeout 3

c:\Python36\python.exe surepatch.py --action=create_project --platform=autotest1 --project=autotest_php_composer_json --target=php_composer_json --method=auto --format=system --file=c:\composer1.json

c:\Python36\python.exe surepatch.py --action=create_project --platform=autotest1 --project=autotest_php_composer_lock --target=php_composer_json --method=auto --format=system --file=c:\composer1.lock

echo --. create project for set test
c:\Python36\python.exe surepatch.py --action=create_project --platform=autotest1 --project=autotest_set_test --method=auto --format=user --file=c:\user_packages.txt
timeout 3

echo 19. create set - OS packages, collected by shell command
c:\Python36\python.exe surepatch.py --action=create_set --platform=autotest1 --project=autotest_set_test --set=os_none.1 --target=os --method=auto --format=system
timeout 3
echo 20. create set autotest_os_path - OS packages, collected from shell command, unloaded to file
c:\Python36\python.exe surepatch.py --action=create_set --platform=autotest1 --project=autotest_set_test --set=os_path.1 --target=os --method=auto --format=system --file=c:\windows_packages.txt
timeout 3
echo 21. create set autotest_pip_none - PIP Packages, collected from shell command
c:\Python36\python.exe surepatch.py --action=create_set --platform=autotest1 --project=autotest_set_test --set=pip_none.1 --target=pip --method=auto --format=system
timeout 3
echo 22. create set autotest_pip_path - PIP packages, collected from shell command, unloaded to file
c:\Python36\python.exe surepatch.py --action=create_set --platform=autotest1 --project=autotest_set_test --set=os_path.1 --target=pip --method=auto --format=system --file=c:\pip_freeze_packages.txt
timeout 3
echo 23. create set autotest_req_path - Python packages from requirements.txt
c:\Python36\python.exe surepatch.py --action=create_set --platform=autotest1 --project=autotest_set_test --set=req_path.1 --target=req --method=auto --format=system --file=c:\requirements.txt
timeout 3
echo 24. create set autotest_npm_none - NPM packages, collected from shell command (npm list --json) from root dir
c:\Python36\python.exe surepatch.py --action=create_set --platform=autotest1 --project=autotest_set_test --set=npm_none.1 --target=npm --method=auto --format=system
timeout 3
echo 25. create set autotest_npm_path - NPM packages, collected from shell command (npm list --json) from root dir, unloaded to file
c:\Python36\python.exe surepatch.py --action=create_set --platform=autotest1 --project=autotest_set_test --set=npm_path.1 --target=npm --method=auto --format=system --file=c:\npm.txt
timeout 3
echo 26. create set autotest_local_none - NPM packages, collected from shell command (npm list --json) from local dir
c:\Python36\python.exe surepatch.py --action=create_set --platform=autotest1 --project=autotest_set_test --set=npm_local_path.1 --target=npm_local --method=auto --format=system --file=c:\workspace\node
timeout 3
echo 27. create set autotest_npm_package_lock_path - NPM packages, collected from package-lock.json file
c:\Python36\python.exe surepatch.py --action=create_set --platform=autotest1 --project=autotest_set_test --set=npm_package_json_lock_path.1 --target=package_lock_json --method=auto --format=system --file=c:\package-lock.json
timeout 3
echo 28. create set autotest_npm_package_json - NPM packages, collected from package.json file
c:\Python36\python.exe surepatch.py --action=create_set --platform=autotest1 --project=autotest_set_test --set=npm_package_json_path.1 --target=package_json --method=auto --format=system --file=c:\package.json
timeout 3
echo 29. create set autotest_gem_none - Ruby packages, collected from shell command
c:\Python36\python.exe surepatch.py --action=create_set --platform=autotest1 --project=autotest_set_test  --set=gem_none.1 --target=gem --method=auto --format=system
timeout 3
echo 30. create set autotest_gem_path - Ruby packages, collected from shell commend, unloaded to file
c:\Python36\python.exe surepatch.py --action=create_set --platform=autotest1 --project=autotest_set_test --set=gem_path.1 --target=gem --method=auto --format=system --file=c:\gem.list
timeout 3
echo 31. create set autotest_gemfile_path - Ruby packages, collected from Gemfile
c:\Python36\python.exe surepatch.py --action=create_set --platform=autotest1 --project=autotest_set_test --set=gem_gemfile_path.1 --target=gemfile --method=auto --format=system --file=c:\Gemfile
timeout 3
echo 32. create set autotest_gemfile_path - Ruby packages, collected from Gemfile.lock
c:\Python36\python.exe surepatch.py --action=create_set --platform=autotest1 --project=autotest_set_test --set=gem_gemfile_lock_path.1 --target=gemfile_lock --method=auto --format=system --file=c:\Gemfile.lock
timeout 3
echo 33. create set autotest_any_user_path - User packages formatted as name=version
c:\Python36\python.exe surepatch.py --action=create_set --platform=autotest1 --project=autotest_set_test --set=user_path.1  --method=auto --format=user --file=c:\user_packages.txt
timeout 3
echo 34. create set autotest_any_user_none - User packages asked from console
c:\Python36\python.exe surepatch.py --action=create_set --platform=autotest1 --project=autotest_set_test --set=user_manual.1 --method=manual --format=user
timeout 3

echo 35. show platforms
c:\Python36\python.exe surepatch.py --action=show_platforms
timeout 3
echo 36. show projects
c:\Python36\python.exe surepatch.py --action=show_projects --platform=autotest1
timeout 3
echo 37. show set
c:\Python36\python.exe surepatch.py --action=show_set --platform=autotest1 --project=autotest_set_test
timeout 3
echo 38. show issues
c:\Python36\python.exe surepatch.py --action=show_issues --platform=autotest1 --project=autotest_set_test

echo complete...