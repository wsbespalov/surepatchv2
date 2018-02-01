#!/bin/sh

chmod 777 surepatch_mac

echo ""start..."

echo ""1. create config"
./surepatch_mac --action=save_config --team=dima --user=ws.bespalov@gmail.com --password=Test123! --logo=off

echo "2. create platform autotest_mac"
./surepatch_mac --action=create_platform --platform=autotest_mac --description=NewPlatformForAutotestMacOS

echo "3. create project autotest_os_none - OS packages, collected by shell command"
./surepatch_mac --action=create_project --platform=autotest_mac --project=autotest_os_none --target=os --method=auto --format=system

echo "4. create project autotest_os_path - OS packages, collected from shell command, unloaded to file"
./surepatch_mac --action=create_project --platform=autotest_mac --project=autotest_os_path --target=os --method=auto --format=system --file=/macos_packages.txt

echo "5. create project autotest_pip_none - PIP Packages, collected from shell command"
./surepatch_mac --action=create_project --platform=autotest_mac --project=autotest_pip_none --target=pip --method=auto --format=system

echo "6. create project autotest_pip_path - PIP packages, collected from shell command, unloaded to file"
./surepatch_mac --action=create_project --platform=autotest_mac --project=autotest_pip_path --target=pip --method=auto --format=system --file=/pip_freeze_packages.txt

echo "7. create project autotest_req_path - Python packages from requirements.txt"
./surepatch_mac --action=create_project --platform=autotest_mac --project=autotest_req_path --target=req --method=auto --format=system --file=/requirements.txt

echo "8. create project autotest_npm_none - NPM packages, collected from shell command (npm list --json) from root dir"
./surepatch_mac --action=create_project --platform=autotest_mac --project=autotest_npm_none --target=npm --method=auto --format=system

echo "9. create project autotest_npm_path - NPM packages, collected from shell command (npm list --json) from root dir, unloaded to file"
./surepatch_mac --action=create_project --platform=autotest_mac --project=autotest_npm_path --target=npm --method=auto --format=system --file=/npm.txt

echo "10. create project autotest_local_none - NPM packages, collected from shell command (npm list --json) from local dir"
./surepatch_mac --action=create_project --platform=autotest_mac --project=autotest_local_none --target=npm_local --method=auto --format=system --file=/

echo "11. create project autotest_npm_package_lock_path - NPM packages, collected from package-lock.json file"
./surepatch_mac --action=create_project --platform=autotest_mac --project=autotest_npm_package_lock_path --target=package_lock_json --method=auto --format=system --file=/package_lock.json

echo "12. create project autotest_npm_package_json - NPM packages, collected from package.json file"
./surepatch_mac --action=create_project --platform=autotest_mac --project=autotest_npm_package_json --target=package_json --method=auto --format=system --file=/package.json

echo "13. create project autotest_gem_none - Ruby packages, collected from shell command"
./surepatch_mac --action=create_project --platform=autotest_mac --project=autotest_gem_none --target=gem --method=auto --format=system

echo "14. create project autotest_gem_path - Ruby packages, collected from shell commend, unloaded to file"
./surepatch_mac --action=create_project --platform=autotest_mac --project=autotest_gem_path --target=gem --method=auto --format=system --file=/gem.list

echo "15. create project autotest_gemfile_path - Ruby packages, collected from Gemfile"
./surepatch_mac --action=create_project --platform=autotest_mac --project=autotest_gemfile_path --target=gemfile --method=auto --format=system --file=/Gemfile

echo "16. create project autotest_gemfile_path - Ruby packages, collected from Gemfile.lock"
./surepatch_mac --action=create_project --platform=autotest_mac --project=autotest_gemfile_lock_path --target=gemfile_lock --method=auto --format=system --file=/Gemfile.lock

echo "17. create project autotest_any_user_path - User packages formatted as name=version"
./surepatch_mac --action=create_project --platform=autotest_mac --project=autotest_any_user_path  --method=auto --format=user --file=/user_packages.txt

echo "18. create project autotest_any_user_none - User packages asked from console"
./surepatch_mac --action=create_project --platform=autotest_mac --project=autotest_any_user_none --method=manual --format=user

echo "19. create project autotest_php_composer_json - PHP Composer file"
./surepatch_mac --action=create_project --platform=autotest_mac --project=autotest_php_composer_json --target=php_composer_json --method=auto --format=system --file=/composer1.json

echo "20. create project autotest_php_composer_lock - PHP Composer.lock file"
./surepatch_mac --action=create_project --platform=autotest_mac --project=autotest_php_composer_lock --target=php_composer_lock --method=auto --format=system --file=/composer1.lock


echo "--. create project for set test"
./surepatch_mac --action=create_project --platform=autotest_mac --project=autotest_set_test --method=auto --format=user --file=/user_packages.txt


echo "21. create set - OS packages, collected by shell command"
./surepatch_mac --action=create_set --platform=autotest_mac --project=autotest_set_test --set=os_none.1 --target=os --method=auto --format=system

echo "22. create set autotest_os_path - OS packages, collected from shell command, unloaded to file"
./surepatch_mac --action=create_set --platform=autotest_mac --project=autotest_set_test --set=os_path.1 --target=os --method=auto --format=system --file=/macos_packages.txt

echo "23. create set autotest_pip_none - PIP Packages, collected from shell command"
./surepatch_mac --action=create_set --platform=autotest_mac --project=autotest_set_test --set=pip_none.1 --target=pip --method=auto --format=system

echo "24. create set autotest_pip_path - PIP packages, collected from shell command, unloaded to file"
./surepatch_mac --action=create_set --platform=autotest_mac --project=autotest_set_test --set=os_path.1 --target=pip --method=auto --format=system --file=/pip_freeze_packages.txt

echo "25. create set autotest_req_path - Python packages from requirements.txt"
./surepatch_mac --action=create_set --platform=autotest_mac --project=autotest_set_test --set=req_path.1 --target=req --method=auto --format=system --file=/requirements.txt

echo "26. create set autotest_npm_none - NPM packages, collected from shell command (npm list --json) from root dir"
./surepatch_mac --action=create_set --platform=autotest_mac --project=autotest_set_test --set=npm_none.1 --target=npm --method=auto --format=system

echo "27. create set autotest_npm_path - NPM packages, collected from shell command (npm list --json) from root dir, unloaded to file"
./surepatch_mac --action=create_set --platform=autotest_mac --project=autotest_set_test --set=npm_path.1 --target=npm --method=auto --format=system --file=/npm.txt

echo "28. create set autotest_local_none - NPM packages, collected from shell command (npm list --json) from local dir"
./surepatch_mac --action=create_set --platform=autotest_mac --project=autotest_set_test --set=npm_local_path.1 --target=npm_local --method=auto --format=system --file=/

echo "29. create set autotest_npm_package_lock_path - NPM packages, collected from package-lock.json file"
./surepatch_mac --action=create_set --platform=autotest_mac --project=autotest_set_test --set=npm_package_json_lock_path.1 --target=package_lock_json --method=auto --format=system --file=/package_lock.json

echo "30. create set autotest_npm_package_json - NPM packages, collected from package.json file"
./surepatch_mac --action=create_set --platform=autotest_mac --project=autotest_set_test --set=npm_package_json_path.1 --target=package_json --method=auto --format=system --file=/package.json

echo "31. create set autotest_gem_none - Ruby packages, collected from shell command"
./surepatch_mac --action=create_set --platform=autotest_mac --project=autotest_set_test  --set=gem_none.1 --target=gem --method=auto --format=system

echo "32. create set autotest_gem_path - Ruby packages, collected from shell commend, unloaded to file"
./surepatch_mac --action=create_set --platform=autotest_mac --project=autotest_set_test --set=gem_path.1 --target=gem --method=auto --format=system --file=/gem.list

echo "33. create set autotest_gemfile_path - Ruby packages, collected from Gemfile"
./surepatch_mac --action=create_set --platform=autotest_mac --project=autotest_set_test --set=gem_gemfile_path.1 --target=gemfile --method=auto --format=system --file=/Gemfile

echo "34. create set autotest_gemfile_path - Ruby packages, collected from Gemfile.lock"
./surepatch_mac --action=create_set --platform=autotest_mac --project=autotest_set_test --set=gem_gemfile_lock_path.1 --target=gemfile_lock --method=auto --format=system --file=/Gemfile.lock

echo "35. create set autotest_any_user_path - User packages formatted as name=version"
./surepatch_mac --action=create_set --platform=autotest_mac --project=autotest_set_test --set=user_path.1  --method=auto --format=user --file=/user_packages.txt

echo "36. create set autotest_any_user_none - User packages asked from console"
./surepatch_mac --action=create_set --platform=autotest_mac --project=autotest_set_test --set=user_manual.1 --method=manual --format=user

echo "37. create set autotest_php_composer_json - PHP Composer file"
./surepatch_mac --action=create_set --platform=autotest_mac --project=autotest_set_test --set=php_composer_json.1 --target=php_composer_json --method=auto --format=system --file=/composer1.json

echo "38. create set autotest_php_composer_lock - PHP Composer.lock file"
./surepatch_mac --action=create_set --platform=autotest_mac --project=autotest_set_test --set=php_composer_lock.1 --target=php_composer_lock --method=auto --format=system --file=/composer1.lock


echo "39. show platforms"
./surepatch_mac --action=show_platforms

echo "40. show projects"
./surepatch_mac --action=show_projects --platform=autotest_mac

echo "41. show set"
./surepatch_mac --action=show_set --platform=autotest_mac --project=autotest_set_test

echo "42. show issues"
./surepatch_mac --action=show_issues --platform=autotest_mac --project=autotest_set_test

echo "complete..."