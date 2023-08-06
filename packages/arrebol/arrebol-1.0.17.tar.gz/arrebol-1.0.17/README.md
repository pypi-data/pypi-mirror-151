# Arrebol


<br>

- https://github.com/traquitanas/arrebol
- https://anaconda.org/michelmetran/arrebol



Pacote criado com a finalidade única de testar como subir um pacote para o conda.

O pacote deve ficar aqui:
- https://anaconda.org/michelmetran/dashboard
- https://anaconda.org/michelmetran/repo


<br>

----

### Passos

Inicialmente é necessário instalar o [conda-build](https://docs.conda.io/projects/conda-build/en/latest/index.html) com o comando:

```bash
conda activate pablocarreira-py39
conda install conda-build
```

<br>

```bash
conda activate pablocarreira-py39
conda-build ./conda -c src/label/main
```

<br>

----

## GitActions

https://github.com/fcakyon/conda-publish-action
Há um GitAction para publicar pacotes no Conda. A vantagem é que ele converte o *build* para outras plataformas (adicionar converters)!

```bash
# Convert Package to Other Platforms
cd ~
platforms=( osx-64 linux-32 linux-64 win-32 win-64 )
find $HOME/conda-bld/linux-64/ -name *.tar.bz2 | while read file
do
    echo $file
    #conda convert --platform all $file  -o $HOME/conda-bld/
    for platform in "${platforms[@]}"
    do
       conda convert --platform $platform $file  -o $HOME/conda-bld/
    done
done
```

<br>

----

### Referências

- https://www.asmeurer.com/conda-docs-test/docs/building/meta-yaml.html
- https://docs.conda.io/projects/conda-build/en/latest/concepts/channels.html
- https://levelup.gitconnected.com/publishing-your-python-package-on-conda-and-conda-forge-309a405740cf
- https://www.youtube.com/watch?v=HSK-6dCnYVQ
- https://giswqs.medium.com/building-a-conda-package-and-uploading-it-to-anaconda-cloud-6a3abd1c5c52
- https://github.com/maxibor/conda-package-publish-action
- https://github.com/rfun/tethysapp-servicetest/blob/master/.github/workflows/main.yml
