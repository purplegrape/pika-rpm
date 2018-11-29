Name:           pika
Version:        3.0.5
Release:        1%{?dist}
Summary:        pika is a nosql compatible with redis
License:        MIT
URL:            https://github.com/Qihoo360/pika
#Source0:        %{name}-%{version}.tar.gz
Source1:        pika.conf
Source2:        pika.service

Source9:        bootstrap.sh
Source10:       pika_deps.tar.gz
Source11:       rocksdb-5.9.2.tar.gz
Source12:       gflags-v1.3.tar.gz
Source13:       gperftools-2.0.zip
Source14:       libunwind-v1.1.zip
Source15:       snappy-1.1.0.tar.gz

BuildRequires:  cmake3
BuildRequires:  gcc-c++
BuildRequires:  git
#BuildRequires:  glog-devel
#BuildRequires:  gflags-devel
#BuildRequires:  libunwind-devel
BuildRequires:  bzip2-devel
BuildRequires:  snappy-devel
BuildRequires:  jemalloc-devel
BuildRequires:  zlib-devel
BuildRequires:  unzip
BuildRequires:  systemd

#BuildRequires:  gperftools-devel

Requires:       glog
Requires:       gflags
Requires:       libunwind
Requires:       bzip2-libs
Requires:       snappy
Requires:       zlib
Requires:       systemd

#Requires:       gperftools-libs

%description
Pika is a persistent huge storage service , compatible with the vast majority of redis interfaces (details), 
including string, hash, list, zset, set and management interfaces. 
With the huge amount of data stored, redis may suffer for a capacity bottleneck, and pika was born for solving it. 
Except huge storage capacity, pika also support master-slave mode by slaveof command, including full and partial synchronization.

%package        static
Summary:	static libriary for pika
%description    static
static library for pika

%prep
rm -rf %{name}-%{version}
git clone --recursive -b v%{version} --depth=1 %{URL} %{name}-%{version}

%build
install -p -m 755 %{SOURCE9} .
./bootstrap.sh

make

g++ \
  src/build_version.o \
  src/pika_admin.o \
  src/pika_binlog_bgworker.o \
  src/pika_binlog.o \
  src/pika_binlog_receiver_thread.o \
  src/pika_binlog_sender_thread.o \
  src/pika_bit.o \
  src/pika.o \
  src/pika_client_conn.o \
  src/pika_command.o \
  src/pika_pubsub.o \
  src/pika_conf.o \
  src/pika_dispatch_thread.o \
  src/pika_hash.o \
  src/pika_heartbeat_conn.o \
  src/pika_heartbeat_thread.o \
  src/pika_hyperloglog.o \
  src/pika_kv.o \
  src/pika_list.o \
  src/pika_master_conn.o \
  src/pika_new_master_conn.o \
  src/pika_monitor_thread.o \
  src/pika_server.o \
  src/pika_set.o \
  src/pika_slaveping_thread.o \
  src/pika_trysync_thread.o \
  src/pika_binlog_transverter.o \
  third/slash/slash/lib/libslash.a \
  third/pink/pink/lib/libpink.a \
  third/blackwidow/lib/libblackwidow.a \
  /tmp/pika_deps/rocksdb/librocksdb.a \
  /tmp/pika_deps/libglog.a \
  /tmp/pika_deps/libtcmalloc.a \
  /tmp/pika_deps/libgflags.a \
  /tmp/pika_deps/libsnappy.a \
  /tmp/pika_deps/libunwind.a \
  src/pika_zset.o  -o pika -lpthread -lrt -lz -lbz2

pushd  tools/aof_to_pika
make
popd

%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT/var/lib/pika
%{__mkdir} -p $RPM_BUILD_ROOT/var/log/pika
%{__mkdir} -p $RPM_BUILD_ROOT/var/run/pika

%{__mkdir} -p $RPM_BUILD_ROOT%{_bindir}
%{__install} -p -m 755 output/bin//pika $RPM_BUILD_ROOT%{_bindir}/pika
%{__install} -p -m 755 tools/aof_to_pika/output/bin/aof_to_pika $RPM_BUILD_ROOT%{_bindir}

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/pika
%{__install} -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pika/pika.conf

%{__mkdir} -p $RPM_BUILD_ROOT%{_unitdir}
%{__install} -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_unitdir}/pika.service

%{__mkdir} -p $RPM_BUILD_ROOT%{_includedir}/pika
%{__install} -p -m 644 third/slash/slash/lib/libslash.a     $RPM_BUILD_ROOT%{_includedir}/pika
%{__install} -p -m 644 third/pink/pink/lib/libpink.a        $RPM_BUILD_ROOT%{_includedir}/pika
%{__install} -p -m 644 third/blackwidow/lib/libblackwidow.a $RPM_BUILD_ROOT%{_includedir}/pika

%{__install} -p -m 644 third/rocksdb/librocksdb.a %{_builddir}/

%pre
# Add the "pika" user
getent group pika  >/dev/null || groupadd -r pika
getent passwd pika >/dev/null || useradd -r -g pika -s /sbin/nologin -d /var/lib/pika pika
exit 0


%files
%{_bindir}/pika
%{_bindir}/aof_to_pika
%config(noreplace) %{_sysconfdir}/pika/pika.conf
%{_unitdir}/pika.service
%dir %attr(755, pika, pika) /var/lib/pika
%dir %attr(755, pika, pika) /var/log/pika
%dir %attr(755, pika, pika) /var/run/pika
%doc README.md README_CN.md Dockerfile 
%license LICENSE

%files static
%{_includedir}/pika

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%clean
rm -rf $RPM_BUILD_ROOT
