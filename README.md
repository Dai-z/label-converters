# Label converters  
Scripts for kinds of converting dataset labels.

- Partly referred to CasiaFan/Dataset_to_VOC_converter

## Requirements

### coco2voc

- cytoolz
- lxml

## Usage

### voc2yolo

```shell
$ python3 voc2yolo.py --img_dir <image directory> --anno_dir <annotation directory>  --out_dir <output directory>
```

By default, this script will automatically parse all annotation files to get class list, sort and output a name file when not given classes are not given. Manually add class in code(line 13)  will skip this parsing stage and use the given classes.

More usage details see:

```shell
$ python3 voc2yolo.py --help
```

