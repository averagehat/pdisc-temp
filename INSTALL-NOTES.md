
Set up with miniconda, not virtualenv 
```
wget https://repo.anaconda.com/miniconda/Miniconda2-py27_4.8.3-Linux-x86_64.sh
bash Miniconda2-py27_4.8.3-Linux-x86_64.sh -b -p $PWD/miniconda
expot PATH=$PWD/miniconda/bin:$PATH
```

Install the actual pipeline. 

NOTE: You may get a failure when snap/ray attempt to install. In that case, follow the relevant instructions and re-run `python setup.py install`

```
 pip install paver
 python setup.py install
```

If snap fails:
```
cd  pathdiscov/download/snap
git checkout v2.0.5
make
cp snap-aligner snap
```

If ray fails:
```
# Note: alternatively you can download manually--
# wget https://github.com/VDBWRAIR/pathdiscov/raw/94754391568cb5b33a3b0bf52a2201d1f2958aa9/pathdiscov/download/RayPlatform.tar.gz && tar -xvf RayPlatform.tar.gz 
cd pathdiscov/download/RayPlatform
to_mpicxx=$(which mpicxx)
make PREFIX=build2000 MPICXX=$to_mpicxx
make install
```

Make sure to get the right version of blast, then add the executables to the path. 
```
wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.12.0+-x64-linux.tar.gz
tar -xvf ncbi-blast-2.17.0+-x64-linux.tar.gz 
```
