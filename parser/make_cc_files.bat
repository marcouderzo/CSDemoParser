@if not exist generated_proto mkdir generated_proto
@echo Running Protocol Buffer Compiler on netmessages_public.proto...
@protoc-2.5.0-win32\protoc.exe --proto_path=. --proto_path=.\protobuf-2.5.0\src --cpp_out=generated_proto netmessages_public.proto
@echo Running Protocol Buffer Compiler on cstrike15_usermessages_public.proto...
@protoc-2.5.0-win32\protoc.exe --proto_path=. --proto_path=.\protobuf-2.5.0\src --cpp_out=generated_proto cstrike15_usermessages_public.proto
