from pathlib import Path
from typing import Literal, Optional

base_url = Path(__file__).resolve().parent

modules_path = base_url / "app" / "modules"
files_to_create = {
    "controllers.py": "# controllers go here",
    "schemas.py": "# schemas go here",
    "router.py": "from fastapi import APIRouter\n",
    "models.py": "# models go here",
    "__init__.py": "",
}


def create_module (module_name: str, router_prefix : Optional[str], api_version:Optional[Literal["api_v1", None]] = "api_v1"):
    if not module_name: return
    module_dir = modules_path / module_name
    module_dir_exist = module_dir.exists()

    if not module_dir_exist:
        module_dir.mkdir()
        module_router_name = f"{module_name}_router" 
        module_router_name  = module_router_name.capitalize()
        
        for key,value in files_to_create.items():

            file_path = module_dir / key
            file_path_exist =  file_path.exists()

            if not file_path_exist:
                with open(file_path, "w") as file: 
                    file.write(value)
                    ## IF THIS IS THE ROUTER LINE INITIALIZE A NEW ROUTER
                    if key == "router.py":
                        prefix = f"{router_prefix}" or ""
                        file.write(f"\n{module_router_name} = APIRouter(prefix=\"/{prefix}\")")

        api_version = api_version if api_version else "api_v1"
        api_dir = base_url / "app" / "api" / api_version / "routes.py"

        if api_dir.exists():
            router_class = "Api_v1" if api_version == "api_v1" else "Router"

            with open(api_dir, "r+") as api:
                content = api.read()
                api.seek(0)
                new_content = (
                    f"from app.modules.{module_name}.router import {module_router_name}\n"
                    f"{content}\n" 
                    f"{router_class}.include_router({module_router_name})"
                )
                api.write(new_content)
                api.truncate()
        else:
            print(f"module could not be included to {api_version}, please do it manually")

        print("module has been create!")
        return
    
    print("module already exist!")
    


if __name__ == "__main__":
    answers = input("enter module_name&router_prefix&api_version (LINK ANSWERS WITH &, NO SPACES, router_prefix&api_version are optional): " )
    answers_arr = answers.strip().split("&")
    module_name= answers_arr[0].strip().lower() if len(answers_arr) > 0 else None
    router_prefix = answers_arr[1].strip().lower() if len(answers_arr) > 1 else None
    api_version = answers_arr[2].strip().lower() if len(answers_arr) > 2 else None
    
    create_module(api_version=api_version, router_prefix=router_prefix, module_name=module_name)

        
