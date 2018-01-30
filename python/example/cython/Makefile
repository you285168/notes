.PHONY: all skynet clean

PLAT ?= linux
SHARED := -fPIC --shared
LUA_CLIB_PATH ?= luaclib
CJSON = depends/lua-cjson-2.1.0/
SNAPSHOT = depends/lua-snapshot-master/

LUA_INC ?= skynet/3rd/lua
LUA_STATICLIB := skynet/3rd/lua/liblua.a
LUA_LIB ?= $(LUA_STATICLIB)
CFLAGS = -g -O2 -Wall -I$(LUA_INC) $(MYCFLAGS)

LUA_CLIB = log time aoi dup2 daemon cjson snapshot

#all : skynet

#skynet/Makefile :
#	git submodule update --init

#skynet : skynet/Makefile
#	cd skynet && $(MAKE) $(PLAT) && cd ..

all : \
  $(foreach v, $(LUA_CLIB), $(LUA_CLIB_PATH)/$(v).so)

$(LUA_CLIB_PATH) :
	mkdir $(LUA_CLIB_PATH)

$(LUA_CLIB_PATH)/log.so : server/lualib-src/lua-log.c | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH)/cjson.so :
	$(MAKE) -C $(CJSON)

$(LUA_CLIB_PATH)/snapshot.so :
	$(MAKE) linux -C $(SNAPSHOT)

$(LUA_CLIB_PATH)/time.so : server/lualib-src/lua-time.c | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH)/dup2.so : server/lualib-src/lua-dup2.c | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH)/daemon.so : server/lualib-src/lua-daemon.c | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH)/aoi.so : server/lualib-src/lua-aoi.c server/lualib-src/aoi.c | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) $(SHARED) $^ -o $@  -Iskynet/skynet-src

install: $(TARGET)
	mkdir -p $(DESTDIR)/$(LUA_CMODULE_DIR)
	cp $(TARGET) $(DESTDIR)$(LUA_CMODULE_DIR)
	chmod $(EXECPERM) $(DESTDIR)$(LUA_CMODULE_DIR)/$(TARGET)

clean :
	rm -f $(LUA_CLIB_PATH)/*.so
	rm -f $(CJSON)/*.o

